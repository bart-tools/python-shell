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

from python_shell.command import Command
from python_shell.shell.processing.process import AsyncProcess
from python_shell.shell.processing.process import SyncProcess
from python_shell import exceptions


__all__ = ('ExceptionTestCase',)


class ExceptionTestCase(unittest.TestCase):
    """Tests for exceptions classes"""

    def test_command_does_not_exist(self):
        """Check that CommandDoesNotExist works properly"""

        cmd_name = "test_{}".format(time.time())
        with self.assertRaises(exceptions.CommandDoesNotExist) as context:
            cmd = Command(cmd_name)
            raise exceptions.CommandDoesNotExist(cmd)
        self.assertEqual(str(context.exception),
                         'Command "{}" does not exist'.format(cmd_name))

    def test_undefined_process(self):
        """Check exception for Undefined process"""

        for method in ('wait', 'terminate'):
            for process_cls in (SyncProcess, AsyncProcess):
                try:
                    process = process_cls('ls')
                    getattr(process, method)()
                except exceptions.UndefinedProcess as e:
                    self.assertEqual(str(e),
                                     "Undefined process cannot be used")
                else:
                    self.fail("UndefinedProcess was not thrown")

    def test_run_process_error(self):
        """Check exception for running process"""

        for process_cls in (SyncProcess, AsyncProcess):
            try:
                process = process_cls('sleepa', 'asd')
                process.execute()
            except exceptions.RunProcessError as e:
                error = "Fail to run 'sleepa asd'"
                self.assertEqual(error, str(e))
            else:
                self.fail("RunProcessError was not thrown")
