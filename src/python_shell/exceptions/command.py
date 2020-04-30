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

# from typing import Optional, Text

from python_shell.exceptions.base import BaseShellException


__all__ = ('CommandException', 'RedirectionParseError')


class CommandException(BaseShellException):
    """Base exception class for errors in Commands"""


class RedirectionParseError(CommandException):
    """Exception for errors while parsing redirection expressions"""

    def __init__(self,
                 redirection_type=None,  # Optional[Text]
                 reason=None
                 ):
        self._redirection_type = redirection_type
        self._reason = reason

    def __str__(self):
        expr_type = ' for type "{}"'.format(
            self._redirection_type) if self._redirection_type else ''
        reason = ': {}'.format(self._reason) if self._reason else ''
        return "Invalid redirection expression{expr_type}{reason}".format(
            expr_type=expr_type,
            reason=reason
        )
