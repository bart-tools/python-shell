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

from python_shell.exceptions import CommandDoesNotExist
from python_shell.exceptions import ShellException
from python_shell.command.interfaces import ICommand
from python_shell.util import AsyncProcess
from python_shell.util import SyncProcess
from python_shell.util import Subprocess


__all__ = ('Command',)


class Command(ICommand):
    """Simple decorator for shell commands"""

    _process = None
    _command = None

    def _validate_command(self, command_name):
        try:
            SyncProcess(
                "which",
                command_name,
                check=True,
                stdout=Subprocess.DEVNULL
            ).execute()
        except Subprocess.CalledProcessError:
            raise CommandDoesNotExist(self)

    def __init__(self, command_name):
        self._command = command_name

    def __call__(self, *args, **kwargs):
        """Executes the command with passed arguments
           and returns a Command instance"""

        self._validate_command(self._command)

        wait = kwargs.pop('wait', True)

        process_cls = SyncProcess if wait else AsyncProcess

        self._arguments = args

        self._process = process_cls(
            self._command,
            *args,
            **kwargs
        )

        try:
            self._process.execute()
        except Subprocess.CalledProcessError:
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
        """Returns an iterable object with output of the command"""
        return self._process.stdout

    @property
    def errors(self):
        """Returns an iterable object with output of the command
           from stderr
        """
        return self._process.stderr

    def __str__(self):
        """Returns command's execution string"""
        return repr(self)

    def __repr__(self):
        """Returns command's execution string"""
        return ' '.join((self.command, self.arguments))
