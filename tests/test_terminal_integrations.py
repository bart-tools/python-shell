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

from python_shell.shell import terminal
from python_shell.shell.terminal.base import BaseTerminalIntegration


__all__ = ('TerminalIntegrationTestCase',)


class FakeBaseTerminal(BaseTerminalIntegration):
    """Fake terminal integration for BaseTerminalIntegration"""

    @property
    def available_commands(self):
        """Wrapper to call parent's property"""

        return super(FakeBaseTerminal, self).available_commands


class TerminalIntegrationTestCase(unittest.TestCase):
    """Abstract Test case for terminal integration"""

    def _test_terminal_available_commands(self, integration_class_name):
        """Check available commands to be non-empty list"""
        term = getattr(terminal, integration_class_name)()
        self.assertLess(0, len(term.available_commands))


class BaseTerminalIntegrationTestCase(TerminalIntegrationTestCase):
    """Test case for Base terminal integration class"""

    def test_shell_name(self):
        """Check 'shell_name' property for Base terminal class"""

        self.assertIsNone(FakeBaseTerminal().shell_name)

    def test_available_commands(self):
        """Check 'available_commands' property for Base terminal class"""

        with self.assertRaises(NotImplementedError):
            _ = FakeBaseTerminal().available_commands


class BashTerminalIntegrationTestCase(TerminalIntegrationTestCase):
    """Test case for Bash terminal integration"""

    def test_bash_available_commands(self):
        """Check if Bash available commands can be retrieved"""
        self._test_terminal_available_commands('BashTerminalIntegration')
