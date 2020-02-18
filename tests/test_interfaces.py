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

from python_shell.interfaces import ICommand


__all__ = ('CommandInterfaceTestCase',)


class FakeCommand(ICommand):
    """A tricky class for testing interfaces"""

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
    def return_code(self):
        return super(FakeCommand, self).return_code


class CommandInterfaceTestCase(unittest.TestCase):
    """Test case for interfaces"""

    @classmethod
    def setUpClass(cls):
        super(CommandInterfaceTestCase, cls).setUpClass()
        cls._command = FakeCommand()

    def test_public_properties_are_abstract(self):
        """Check that all properties are abstract"""

        for prop_name in ('output', 'arguments', 'command', 'return_code'):
            with self.assertRaises(NotImplementedError):
                getattr(self._command, prop_name)
