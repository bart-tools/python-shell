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

from python_shell.command.interfaces import ICommand
from python_shell.shell.processing.interfaces import IProcess
from python_shell.shell.terminal.interfaces import ITerminalIntegration


__all__ = ('FakeCommand', 'FakeProcess', 'FakeTerminal')


class FakeCommand(ICommand):
    """Fake command for testing interfaces"""

    def __init__(self):
        pass

    @property
    def command(self):
        return super(FakeCommand, self).command

    @property
    def arguments(self):
        return super(FakeCommand, self).arguments

    @property
    def output(self):
        return super(FakeCommand, self).output

    @property
    def errors(self):
        return super(FakeCommand, self).errors

    @property
    def return_code(self):
        return super(FakeCommand, self).return_code


class FakeTerminal(ITerminalIntegration):
    """Fake terminal for testing terminal integration interface"""

    @property
    def available_commands(self):
        return super(FakeTerminal, self).available_commands

    @property
    def shell_name(self):
        return super(FakeTerminal, self).available_commands


class FakeProcess(IProcess):
    """Fake process for testing process interface"""

    @property
    def stderr(self):
        return super(FakeProcess, self).stderr

    @property
    def stdout(self):
        return super(FakeProcess, self).stdout

    @property
    def returncode(self):
        return super(FakeProcess, self).returncode

    @property
    def is_finished(self):
        return super(FakeProcess, self).is_finished

    @property
    def execute(self):
        return super(FakeProcess, self).execute()
