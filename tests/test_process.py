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

from python_shell.shell.processing.process import AsyncProcess
from python_shell.shell.processing.process import SyncProcess
from python_shell.shell.processing.process import Subprocess
from python_shell.util.streaming import decode_stream


class SyncProcessTestCase(unittest.TestCase):
    """Test case for synchronous process wrapper"""

    def _test_sync_process_is_finished(self):
        sync_process_args = ['echo', 'Hello']
        sync_process_kwargs = {
            'stdout': Subprocess.DEVNULL,
            'stderr': Subprocess.DEVNULL
        }
        process = SyncProcess(*sync_process_args,
                              **sync_process_kwargs)
        process.execute()
        self.assertIsNotNone(process.returncode)
        self.assertTrue(process.is_finished)


    def _test_sync_process_not_initialized(self):
        """Check process which was not initialized"""
        process = SyncProcess(['ls'])
        self.assertIsNone(process.is_finished)

    def test_sync_process_property_is_finished(self):
        """Check that is_finished works well for SyncProcess"""
        self._test_sync_process_is_finished()
        # TODO(albartash): Check for not finished process is TBD:
        #                  It needs a proper implementation,
        #                  as SyncProcess blocks main thread.
        self._test_sync_process_not_initialized()

    def test_sync_process_termination(self):
        """Check that SyncProcess can be terminated properly"""
        self.skipTest("TODO")

    def test_sync_process_completion(self):
        """Check that SyncProcess can be completed properly"""
        self.skipTest("TODO")


class AsyncProcessTestCase(unittest.TestCase):
    """Test case for asynchronous process wrapper"""

    processes = []

    @classmethod
    def tearDownClass(cls):
        """Cleanup processes"""
        for p in cls.processes:
            try:
                p._process.terminate()
            except OSError:
                pass
            p._process.stderr.close()
            p._process.stdout.close()

    def test_async_process_is_finished(self):
        timeout = 0.1  # seconds
        process = AsyncProcess('sleep', str(timeout))
        self.processes.append(process)
        process.execute()
        self.assertIsNone(process.returncode)
        time.sleep(timeout + 1)  # ensure command finishes
        self.assertEqual(process.returncode, 0)

    def test_async_process_is_not_initialized(self):
        """Check that async process is not initialized when not finished"""
        timeout = 0.5  # seconds
        process = AsyncProcess('sleep', str(timeout))
        self.processes.append(process)
        process.execute()
        self.assertIsNone(process.returncode)
        time.sleep(timeout + 0.5)
        self.assertIsNotNone(process.returncode)

    def test_async_std_properties_accessible(self):
        """Check if standard properties are accessible for AsyncProcess"""

        timeout = 0.5  # seconds
        process = AsyncProcess('sleep', str(timeout))
        self.processes.append(process)
        process.execute()
        stdout = decode_stream(process.stdout)
        stderr = decode_stream(process.stderr)

        self.assertEqual(stdout, "")
        self.assertEqual(stderr, "")

    def test_async_process_property_is_finished(self):
        self.skipTest("TODO")

    def test_async_process_termination(self):
        """Check that AsyncProcess can be terminated properly"""

        process = AsyncProcess('yes')
        process.execute()
        process.terminate()

        self.assertTrue(process.is_terminated)
        self.assertEqual(process.returncode, -15)

    def test_async_process_completion(self):
        """Check that AsyncProcess can be completed properly"""

        timeout = str(0.5)
        process = AsyncProcess('sleep', timeout)
        process.execute()
        process.wait()
        self.assertTrue(process.is_finished)
        self.assertEqual(process.returncode, 0)
