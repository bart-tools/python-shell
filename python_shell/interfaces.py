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

import abc

from six import with_metaclass

__all__ = ('ICommand',)


class ICommand(with_metaclass(abc.ABCMeta)):
    """Interface for shell Commands"""

    @property
    @abc.abstractmethod
    def command(self):
        """Returns a string with the command"""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def arguments(self):
        """Returns a string with the arguments passed to the command"""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def return_code(self):
        """Returns an integer code returned by the invoked command"""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def output(self):
        """Returns a string output of the invoked command from stdout"""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def errors(self):
        """Returns a string output of the invoked command from stderr"""
        raise NotImplementedError
