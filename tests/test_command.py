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

import os
import sys
import tempfile
import time
import unittest


from python_shell.command import Command
from python_shell.exceptions import CommandDoesNotExist

__all__ = ('CommandTestCase',)


class CommandTestCase(unittest.TestCase):
    FILES_COUNT = 5

    def setUp(self):
        self.tmp_folder = tempfile.mkdtemp()

    def tearDown(self):
        os.rmdir(self.tmp_folder)

    def test_existing_command(self):
        """Check that existing command runs correctly"""

        command = Command('ls')
        command(self.tmp_folder)
        self.assertEqual(command.return_code, 0)

    def test_non_existing_command_python_2(self):
        """Check when command does not exist in Python 2"""

        if sys.version_info[0] != 2:
            self.skipTest('Only for Python 2')
        with self.assertRaises(OSError):
            Command('random_{}'.format(time.time()))()

    def test_non_existing_command_python_3(self):
        """Check when command does not exist in Python 3"""

        if sys.version_info[0] != 3:
            self.skipTest('Only for Python 3')
        with self.assertRaises(CommandDoesNotExist):
            Command('random_{}'.format(time.time()))()

    def test_command_output(self):
        """Check command output property"""
        value = str(time.time())
        command = Command('echo')(value)
        self.assertEqual(command.output, "{}\n".format(value))

    def test_string_representation(self):
        """Check command string representation"""
        value = str(time.time())
        command = Command('echo')(value)
        self.assertEqual(str(command), value + '\n')

    def test_command_base_representation(self):
        """Check command general representation"""
        args = ('-l', '-a', '/tmp')
        command = Command('ls')(*args)
        self.assertEqual(repr(command), ' '.join((command.command,) + args))
