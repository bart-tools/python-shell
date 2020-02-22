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

import unittest


from python_shell.exceptions import ShellException
from python_shell.shell import Shell


__all__ = ('ShellTestCase',)


class ShellTestCase(unittest.TestCase):
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
        self.skipTest("Cannot test it right now - need more functionality")
        # FIXME(albartash): Implement this test
