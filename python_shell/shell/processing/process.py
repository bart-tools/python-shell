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

import abc
import os
import subprocess

from six import with_metaclass

from python_shell.exceptions import RunProcessError
from python_shell.exceptions import UndefinedProcess
from python_shell.shell.processing.interfaces import IProcess
from python_shell.util.version import is_python2_running


__all__ = ('Subprocess', 'Process', 'SyncProcess', 'AsyncProcess')


_PIPE = subprocess.PIPE

if is_python2_running():
    class _CalledProcessError(OSError):
        """A wrapper for Python 2 exceptions.

        Code is taken from CalledProcessError of Python 3 and adopted.
        """

        def __init__(self, returncode, cmd, output=None, stderr=None):
            super(_CalledProcessError, self).__init__()

            self.returncode = returncode
            self.cmd = cmd
            self.stdout = output
            self.stderr = stderr

        def __str__(self):
            return "Command '%s' returned non-zero exit status %d." % (
                self.cmd, self.returncode)

else:
    _CalledProcessError = subprocess.CalledProcessError


class StreamIterator(object):
    """A wrapper for retrieving data from subprocess streams"""

    def __init__(self, stream=None):
        """Initialize object with passed stream.

        If stream is None, that means process is undefined,
        and iterator will just raise StopIteration.
        """

        self._stream = stream

    def __iter__(self):
        return self

    def __next__(self):
        """Returns next available line from passed stream"""

        if not self._stream:
            raise StopIteration

        line = self._stream.readline()
        if line:
            return line
        raise StopIteration

    next = __next__


class Process(IProcess):
    """A wrapper for process

    When process is not initialized (passed process=None to constructor),
    it is generally undefined, so neither completed nor running,
    but for practical reason, assume it has never been started.
    """

    _process = None  # process instance
    _args = None
    _kwargs = None

    PROCESS_IS_TERMINATED_CODE = -15

    def __init__(self, command, *args, **kwargs):
        self._command = command
        self._args = args
        self._kwargs = kwargs

    @property
    def stderr(self):
        """Returns stderr output of process"""

        return StreamIterator(
            stream=self._process and self._process.stderr or None
        )

    @property
    def stdout(self):
        """Returns stdout output of process"""

        return StreamIterator(
            stream=self._process and self._process.stdout or None
        )

    @property
    def returncode(self):  # -> Union[int, None]
        """Returns returncode of process

        For undefined process, it returns None
        """

        if self._process:
            self._process.poll()  # Ensure we can get the returncode
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

    @property
    def is_terminated(self):  # -> Union[bool, None]
        """Returns whether process has been terminated

        For undefined process, it returns None.
        """

        if self._process:
            return self.returncode == self.PROCESS_IS_TERMINATED_CODE
        return None

    @property
    def is_undefined(self):
        """Returns whether process is undefined"""
        return self._process is None

    def _make_command_execution_list(self, args):
        """Builds and returns a Shell command"""

        return [self._command] + list(map(str, args))

    def terminate(self):
        """Terminates process if it's defined"""

        if self._process:
            self._process.terminate()

            # NOTE(albartash): It's needed, otherwise termination can happen
            #                  slower than next call of poll().
            self._process.wait()
        else:
            raise UndefinedProcess

    def wait(self):
        """Wait until process is completed"""

        if self._process:
            self._process.wait()
        else:
            raise UndefinedProcess

    @abc.abstractmethod
    def execute(self):
        """Abstract method, to be implemented in derived classes"""

        raise NotImplementedError


class SyncProcess(Process):
    """Process subclass for running process
    with waiting for its completion"""

    def execute(self):
        """Run a process in synchronous way"""

        arguments = self._make_command_execution_list(self._args)

        kwargs = {
            'stdout': self._kwargs.get('stdout', Subprocess.PIPE),
            'stderr': self._kwargs.get('stderr', Subprocess.PIPE),
            'stdin': self._kwargs.get('stdin', Subprocess.PIPE)
        }

        try:
            self._process = subprocess.Popen(
                arguments,
                **kwargs
            )
        except (OSError, ValueError):
            raise RunProcessError(
                cmd=arguments[0],
                process_args=arguments[1:],
                process_kwargs=kwargs
            )

        if is_python2_running():  # Timeout is not supported in Python 2
            self._process.wait()
        else:
            self._process.wait(timeout=self._kwargs.get('timeout', None))

        if self._process.returncode and self._kwargs.get('check', True):
            raise Subprocess.CalledProcessError(
                returncode=self._process.returncode,
                cmd=str(arguments)
            )


class AsyncProcess(Process):
    """Process subclass for running process
    with waiting for its completion"""

    def execute(self):
        """Run a process in asynchronous way"""

        arguments = self._make_command_execution_list(self._args)

        kwargs = {
            'stdout': self._kwargs.get('stdout', Subprocess.PIPE),
            'stderr': self._kwargs.get('stderr', Subprocess.PIPE),
            'stdin': self._kwargs.get('stdin', Subprocess.PIPE)
        }

        try:
            self._process = subprocess.Popen(
                arguments,
                **kwargs
            )
        except (OSError, ValueError):
            raise RunProcessError(
                cmd=arguments[0],
                process_args=arguments[1:],
                process_kwargs=kwargs
            )


class _SubprocessMeta(type):
    """Meta class for Subprocess"""

    _devnull = None

    @property
    def DEVNULL(cls):  # -> int
        """Returns a DEVNULL constant compatible with all Pytho versions"""

        if is_python2_running():
            if cls._devnull is None:
                cls._devnull = os.open(os.devnull, os.O_RDWR)
        else:
            cls._devnull = subprocess.DEVNULL

        return cls._devnull


class Subprocess(with_metaclass(_SubprocessMeta, object)):
    """A wrapper for subprocess module"""

    CalledProcessError = _CalledProcessError
    PIPE = _PIPE
