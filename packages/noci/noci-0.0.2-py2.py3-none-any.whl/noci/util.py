#!/usr/bin/env python
# -*- encoding:utf-8 -*-
from __future__ import print_function
import errno
import glob
import os
try:
    from queue import Queue
except ImportError:
    from Queue import Queue
import shutil
import subprocess
import sys
from threading import Thread
import time


# copy all contents from src_dir to dest_dir,
# if file already exist in dest_dir, overwrite it
def copy_dir(src_dir, dest_dir):
    mkdir(dest_dir)
    for root, dirs, files in os.walk(src_dir):
        relpath = os.path.relpath(root, src_dir)
        for dir in dirs:
            dest_full_path = os.path.join(dest_dir, relpath, dir)
            if not os.path.exists(dest_full_path):
                mkdir(dest_full_path)

        for file in files:
            src_full_path = os.path.join(src_dir, relpath, file)
            dest_full_path = os.path.join(dest_dir, relpath, file)
            shutil.copy2(src_full_path, dest_full_path)


# if dest exists, overwrite it only when it is a file or symlink
def copy_file(src, dest):
    if os.path.exists(dest) and not os.path.isfile(dest):
        raise Exception("dest must be a valid file")
    mkdir(os.path.dirname(dest))
    shutil.copy2(src, dest)


# copy file in to directory, will make sure the directory exists
def copy_file_into_dir(src, dest_dir):
    if os.path.exists(dest_dir) and not os.path.isdir(dest_dir):
        raise Exception("dest_dir must be a valid directory")
    mkdir(dest_dir)
    shutil.copy2(src, dest_dir)


# copy all contents from src_dir to dest_dir,
# make sure src_dir and dest_dir are exactly the same
def sync_dir(src_dir, dest_dir):
    mkdir(dest_dir)
    reset_dir(dest_dir)
    copy_dir(src_dir, dest_dir)


# empty a directory
# be cautious of this method, it may wipe out the whole file system.
# if dir_path's length is less than min_path_len, directory won't be wiped out.
def reset_dir(dir_path, min_path_len=10):
    if not dir_path.strip():
        raise Exception("path should not be empty" % dir_path)

    if dir_path in ["/", "/root", "/etc", "/usr", "/sys", "/dev", "/proc"]:
        raise Exception("path '%s' refer to location which should not be removed" % dir_path)

    if len(dir_path) < min_path_len:
        raise Exception("path '%s' is too short, should not be removed" % dir_path)

    mkdir(dir_path)
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
            raise


# equivalent of mkdir -p
def mkdir(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python ≥ 2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        # possibly handle other errno cases here, otherwise finally:
        else:
            raise


# remove files by glob pattern
def remove_by_pattern(pattern):
    files = glob.glob(pattern)
    for file in files:
        os.remove(file)


# equivalent of chmod +x path
def make_executable(path):
    import stat

    st = os.stat(path)
    os.chmod(path, st.st_mode | stat.S_IEXEC)


# check whether file is outdated
# if file does not exists or other errors occurred, consider as outdated
def file_outdated(path, expiration_minutes):
    try:
        modified_time = os.path.getmtime(path)
        if time.time() - modified_time > expiration_minutes*60:
            return True
        else:
            return False
    except Exception:
        return True


def print_stderr(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class RunFailed(Exception):
    """Raised when run() returns a non-zero exit status.

    Attributes:
      cmd, returncode, stdout, stderr, output
    """
    def __init__(self, returncode, cmd, output=None, stderr=None):
        self.returncode = returncode
        self.cmd = cmd
        self.output = output
        self.stderr = stderr

    def __str__(self):
        if self.returncode and self.returncode < 0:
            return "Command '%s' died with signal %d." % (
                self.cmd, -self.returncode)
        else:
            return "Command '%s' returned non-zero exit status %d." % (
                self.cmd, self.returncode)

    @property
    def stdout(self):
        """Alias for output attribute, to match stderr"""
        return self.output

    @stdout.setter
    def stdout(self, value):
        # There's no obvious reason to set this, but allow it anyway so
        # .stdout is a transparent alias for .output
        self.output = value


# need to read stderr from another thread, otherwise it would block at p.stdout.readline()
# https://stackoverflow.com/questions/60606499/python-gets-stuck-at-pipe-stdin-write
def _consume_stderr(q):
    stderr_pipe = q.get()
    print_to_console = q.get()
    stderr = ""
    while True:
        stderr_line = stderr_pipe.readline()
        stderr_line = stderr_line.decode("utf-8")
        stderr += stderr_line
        if not stderr_line:
            break
        if print_to_console:
            try:
                print_stderr(stderr_line, end="")
            except UnicodeEncodeError:
                print_stderr(stderr_line.encode("ascii", "backslashreplace"), end="")
    q.put(stderr)


def run(cmd, stdin=None, print_to_console=True, shell=True):
    stdin_pipe = subprocess.PIPE if stdin else None
    p = subprocess.Popen(cmd, stdin=stdin_pipe, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell)
    if stdin:
        p.stdin.write(stdin)
        p.stdin.close()

    # use queue to syncronize between threads
    q = Queue()

    q.put(p.stderr)
    q.put(print_to_console)
    t = Thread(target=_consume_stderr, args=(q,))
    t.start()

    output = ""
    while True:
        stdout_line = p.stdout.readline()
        stdout_line = stdout_line.decode("utf-8")
        output += stdout_line
        if not stdout_line:
            break
        if print_to_console:
            try:
                print(stdout_line, end="")
            except Exception:
                print(stdout_line.encode("ascii", "backslashreplace"), end="")
    p.wait()
    t.join()
    stderr = q.get(block=False)
    if p.returncode != 0:
        raise RunFailed(p.returncode, cmd, output, stderr)
    return output