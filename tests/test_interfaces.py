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

from .fixtures import interfaces


__all__ = ('CommandInterfaceTestCase', 'TerminalInterfaceTestCase')


class BaseInterfaceTestCase(unittest.TestCase):
    """Base test case for interfaces"""
    implementation_class = None  # Interface fake implementation class
    properties = ()  # List of properties to be checked

    @classmethod
    def setUpClass(cls):
        """Initialize implementation"""
        super(BaseInterfaceTestCase, cls).setUpClass()
        cls._instance = cls.implementation_class()

    def _check_properties(self):
        """Check that all properties are abstract"""
        for prop_name in self.properties:
            with self.assertRaises(NotImplementedError):
                getattr(self._instance, prop_name)


class CommandInterfaceTestCase(BaseInterfaceTestCase):
    """Test case for Command interface"""

    implementation_class = interfaces.FakeCommand
    properties = ('output', 'arguments', 'command', 'return_code', 'errors')

    def test_command_interface(self):
        self._check_properties()


class TerminalInterfaceTestCase(BaseInterfaceTestCase):
    """Test case for Terminal integration interface"""

    implementation_class = interfaces.FakeTerminal
    properties = ('available_commands', 'shell_name')

    def test_terminal_integration_interface(self):
        self._check_properties()


class ProcessInterfaceTestCase(BaseInterfaceTestCase):
    """Test case for Process interface"""

    implementation_class = interfaces.FakeProcess
    properties = ('stderr', 'stdout', 'returncode')
