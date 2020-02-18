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

from python_shell.command import Subprocess


__all__ = ('SubprocessTestCase',)


class SubprocessTestCase(unittest.TestCase):
    """Test case for Subprocess wrapper"""

    def test_run_python3(self):
        """Check that run() works for python 3"""

        if sys.version_info[0] != 3:
            self.skipTest("Only for Python 3")
        try:
            Subprocess.run(['echo'])
        except Exception as e:
            self.fail(str(e))

    def test_run_python2(self):
        """Check that run() works for python 2"""

        if sys.version_info[0] != 2:
            self.skipTest("Only for Python 2")

        extra_args = {'check': True}
        Subprocess.run(['echo'], **extra_args)
