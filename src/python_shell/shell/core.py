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

from six import with_metaclass

from python_shell.command import Command
from python_shell.shell.terminal import TERMINAL_INTEGRATION_MAP
from python_shell.util.terminal import get_current_terminal_name


__all__ = ('Shell',)


class MetaShell(type):

    __own_fields__ = ('last_command',)

    def __getattr__(cls, item):
        """Returns either own field or shell command object"""

        # NOTE(albartash): The next check ensures we wouldn't have troubles
        #                  in getting own fields even if forgetting to define
        #                  a related property for that.

        if item in cls.__own_fields__:
            return cls.__dict__[item]

        cls._last_command = Command(item)
        return cls._last_command

    def __dir__(cls):
        """Return list of available shell commands + own fields"""
        name = get_current_terminal_name()
        commands = TERMINAL_INTEGRATION_MAP[name]().available_commands
        return sorted(
            list(cls.__own_fields__) + commands
        )

    @property
    def last_command(cls):
        """Returns last executed command"""
        return cls._last_command


class Shell(with_metaclass(MetaShell)):
    """Simple decorator for Terminal using Subprocess"""

    _last_command = None

    def __new__(cls, command_name):
        """Returns an ICommand instance for specified command_name.
        This is useful for shell commands which names are not valid
        in Python terms as identifier.

        NOTE: This is not a constructor, as it could seem to be.
        """
        return getattr(cls, command_name)
