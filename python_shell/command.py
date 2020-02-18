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
import sys

from python_shell.exceptions import CommandDoesNotExist
from python_shell.exceptions import ShellException
from python_shell.interfaces import ICommand


__all__ = ('Command',)


class Subprocess(object):
    """A wrapper for subprocess module"""

    @staticmethod
    def run(*args, **kwargs):
        """A simple wrapper for run() method of subprocess"""
        if sys.version_info[0] == 3:
            return subprocess.run(*args, **kwargs)
        else:
            if 'check' in kwargs:
                kwargs.pop('check')
            process = subprocess.Popen(*args, **kwargs)
            stdout = process.communicate()[0]
            process._stdout = stdout
            return process

    @staticmethod
    def DEVNULL():
        """A wrapper for DEVNULL which does not exist in Python 2"""

        if sys.version_info[0] == 3:
            return subprocess.DEVNULL
        else:
            return open(os.devnull, 'w')


class Command(ICommand):
    """Simple decorator for shell commands"""

    _arguments = None
    _process = None
    _command = None

    def _validate_command(self, command_name):
        try:
            Subprocess.run(("which", command_name),
                           check=True,
                           stdout=Subprocess.DEVNULL())
        except subprocess.CalledProcessError:
            raise CommandDoesNotExist(self)
        except OSError:  # for Python 2
            raise CommandDoesNotExist(self)

    @staticmethod
    def _make_arguments(args, kwargs):
        """Makes a list of arguments for Shell command"""
        return list(map(str, args)) + list(itertools.chain(kwargs.items()))

    def _make_command_execution_list(self, args, kwargs):
        """Builds and returns a Shell command"""

        self._arguments = self._make_arguments(args, kwargs)
        return [self._command] + self._arguments

    def __init__(self, command_name):
        self._command = command_name
        self._validate_command(command_name)

    def __call__(self, *args, **kwargs):
        """Executes the command with passed arguments
           and returns a Command instance"""

        self._process = Subprocess.run(
            self._make_command_execution_list(
                args, kwargs),
            stdout=subprocess.PIPE)
        if self._process.returncode:
            raise ShellException(self)
        return self

    @property
    def command(self):
        """Returns a string with the command"""
        return self._command

    @property
    def arguments(self):
        """Returns a string with the arguments passed to the command"""
        return ' '.join(self._arguments)

    @property
    def return_code(self):
        """Returns an integer code returned by the invoked command"""
        return self._process.returncode

    @property
    def output(self):
        """Returns a string output of the invoked command"""
        if sys.version_info[0] == 3:
            return self._process.stdout.decode()
        else:
            return self._process._stdout
