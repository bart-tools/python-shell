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

import sys
import unittest

from python_shell.shell.terminal import TERMINAL_INTEGRATION_MAP
from python_shell.util import is_python2_running
from python_shell.util import get_current_terminal_name


__all__ = ('UtilTestCase',)


class UtilTestCase(unittest.TestCase):
    """Test case for utils"""

    def test_python_version_checker(self):
        """Check if python version checker works properly"""
        self.assertEqual(is_python2_running(), sys.version_info[0] == 2)

    def test_get_current_terminal_name(self):
        """Check that getting current terminal name works"""
        self.assertIn(get_current_terminal_name(),
                      TERMINAL_INTEGRATION_MAP.keys())
