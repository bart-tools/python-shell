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


import itertools

from python_shell.exceptions import CommandDoesNotExist
from python_shell.exceptions import ShellException
from python_shell.interfaces import ICommand
from python_shell.util import Process
from python_shell.util import Subprocess


__all__ = ('Command',)


class Command(ICommand):
    """Simple decorator for shell commands"""

    _arguments = []
    _process = None
    _command = None

    def _validate_command(self, command_name):
        try:
            Subprocess.run(("which", command_name),
                           check=True,
                           stdout=Subprocess.DEVNULL())
        except Subprocess.CalledProcessError:
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
        self._process = Process()

    def __call__(self, *args, **kwargs):
        """Executes the command with passed arguments
           and returns a Command instance"""
        self._validate_command(self._command)
        self._process = Process(
            Subprocess.run(
                self._make_command_execution_list(
                    args, kwargs),
                stdout=Subprocess.PIPE,
                stderr=Subprocess.PIPE
            )
        )
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
        return self._process.stdout

    @property
    def errors(self):
        """Returns a string output of the invoked command from stderr """
        return self._process.stderr

    def __str__(self):
        """Returns command's output as a string"""
        return self.output

    def __repr__(self):
        """Returns command's execution string"""
        return ' '.join((self.command, self.arguments))
