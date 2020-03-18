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

import time
import unittest


from python_shell.exceptions import CommandDoesNotExist
from python_shell.exceptions import ShellException
from python_shell.shell import Shell
from python_shell.shell.terminal import TERMINAL_INTEGRATION_MAP
from python_shell.util.streaming import decode_stream
from python_shell.util.terminal import get_current_terminal_name


__all__ = ('ShellTestCase',)


class ShellTestCase(unittest.TestCase):
    """Test case for Shell"""

    def test_own_fields(self):
        """Check Shell own fields to be accessible"""
        for field in ('last_command',):
            getattr(Shell, field)

    def test_shell_non_zero_return_code(self):
        """Check the case when Shell command returns non-zero code"""
        with self.assertRaises(ShellException) as context:
            Shell.mkdir('/tmp')
        self.assertEqual(str(context.exception),
                         'Shell command "mkdir /tmp" failed '
                         'with return code 1')

    def test_last_command(self):
        """Check "last_command" property to be working"""
        command = Shell.mkdir('-p', '/tmp')
        self.assertEqual(Shell.last_command.command, 'mkdir')
        self.assertEqual(Shell.last_command.arguments, '-p /tmp')
        self.assertEqual(command, Shell.last_command)

    def test_command_errors(self):
        """Check command errors property"""
        command = Shell.ls
        non_existing_dir_name = "/nofolder_{:.0f}".format(time.time())
        with self.assertRaises(ShellException):
            command(non_existing_dir_name)

        # NOTE(albartash): This test partially relies on "ls" output,
        #                  but it's done as less as possible
        error_output = decode_stream(command.errors)
        for part in ('ls', non_existing_dir_name, 'No such'):
            self.assertIn(part, error_output)

    def test_dir_shell(self):
        """Check usage of dir(Shell)"""
        name = get_current_terminal_name()
        commands = TERMINAL_INTEGRATION_MAP[name]().available_commands
        self.assertLess(0, len(commands))
        commands_dir = dir(Shell)
        self.assertEqual(sorted(commands + ['last_command']), commands_dir)

    def test_shell_for_non_identifier_command(self):
        """Check ability to call Shell for non-identifier-like commands"""
        command_name = '2echo'
        command = Shell(command_name)
        with self.assertRaises(CommandDoesNotExist):
            command()
        self.assertEqual(Shell.last_command.command, command_name)
