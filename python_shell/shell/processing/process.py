"""
MIT License

Copyright (c) 2020 Alex Sokolov

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from io import open
import itertools
import os
import subprocess
# from typing import Text, Union

from python_shell.shell.processing.interfaces import IProcess
from python_shell.util.version import is_python2_running


__all__ = ('Subprocess', 'Process', 'SyncProcess', 'AsyncProcess')


_PIPE = subprocess.PIPE

if is_python2_running():
    class _CalledProcessError(OSError):
        """A wraooer for Python 2 exceptions.

        Code is taken from CalledProcessError of Python 3 and adopted.
        """

        def __init__(self, returncode, cmd, output=None, stderr=None):
            self.returncode = returncode
            self.cmd = cmd
            self.stdout = output
            self.stderr = stderr

        def __str__(self):
            return "Command '%s' returned non-zero exit status %d." % (
                self.cmd, self.returncode)

else:
    _CalledProcessError = subprocess.CalledProcessError


class Process(IProcess):
    """A wrapper for process

    When process is not initialized (passed process=None to constructor),
    it is generally undefined, so neither completed nor running,
    but for practical reason, assume it has never been started.
    """

    _process = None  # process instance
    _args = None
    _kwargs = None

    def __init__(self, command, *args, **kwargs):
        self._command = command
        self._args = args
        self._kwargs = kwargs

    @property
    def stderr(self):  # -> Text
        """Returns stderr output of process

        For undefined process, it returns empty string.
        """
        if is_python2_running():
            return self._process._stderr if self._process else ""
        return self._process.stderr.decode() \
            if self._process and self._process.stderr else ""

    @property
    def stdout(self):  # -> Text
        """Returns stdout output of process

        For undefined process, it returns empty string.
        """
        if is_python2_running():
            return self._process._stdout if self._process else ""
        return self._process.stdout.decode() \
            if self._process and self._process.stdout else ""

    @property
    def returncode(self):  # -> Union[int, None]
        """Returns returncode of process

        For undefined process, it returns None
        """
        if self._process:
            return self._process.returncode
        return None

    @property
    def is_finished(self):  # -> Union[bool, None]
        """Returns whether process has been completed

        For undefined process, it returns None.
        """
        if self._process:
            return self._process.returncode is not None
        return None

    def _make_command_execution_list(self, args):
        """Builds and returns a Shell command"""

        return [self._command] + list(map(str, args))


class SyncProcess(Process):
    """Process subclass for running process
    with waiting for its completion"""

    def execute(self):
        """Run a process in synchronous way"""

        arguments = self._make_command_execution_list(self._args)

        stdout = self._kwargs.get('stdout', Subprocess.PIPE)
        stderr = self._kwargs.get('stderr', Subprocess.PIPE)
        stdin = self._kwargs.get('stdin', Subprocess.PIPE)

        if is_python2_running():
            self._process = subprocess.Popen(
                arguments,
                stdout=stdout,
                stderr=stderr,
                stdin=stdin
            )

            stdout, stderr = self._process.communicate()

            self._process._stdout = stdout
            self._process._stderr = stderr
        else:
            self._process = subprocess.run(
                arguments,
                stdin=stdin,
                stdout=stdout,
                stderr=stderr,
                check=False
            )
        if self._process.returncode and self._kwargs.get('check', True):
            raise Subprocess.CalledProcessError(
                returncode=self._process.returncode,
                cmd=str(arguments)
            )


class AsyncProcess(Process):
    """Process subclass for running process
    without waiting for its completion"""

    def __init__(self):
        raise NotImplementedError


class Subprocess(object):
    """A wrapper for subprocess module"""

    CalledProcessError = _CalledProcessError
    PIPE = _PIPE

    @classmethod
    def DEVNULL(cls):  # -> Union[subprocess.DEVNULL, _io.TextIOWrapper]
        """A wrapper for DEVNULL which does not exist in Python 2"""
        if is_python2_running():
            return open(os.devnull, 'w')
        else:
            return subprocess.DEVNULL
