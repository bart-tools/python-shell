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

from enum import Enum
import os
import re
import sys
# from typing import Text


from python_shell.exceptions.command import RedirectionParseError


class RedirectionType(Enum):
    """Possible types of redirections"""

    TO = '>'
    FROM = '<'
    APPEND = '>>'


REDIRECTION_TYPES = ('>', '>>')
REDIRECTION_MODES = {
    '>': 'w',
    '>>': 'a'
}


class Redirection:

    DEFAULT_OUTPUT_STREAM = "1"

    STANDARD_STREAMS = {
        '1': sys.stdout,
        '2': sys.stderr
    }

    STANDARD_FILES = {
        '/dev/stdout': sys.stdout,
        '/dev/stderr': sys.stderr
    }

    def __init__(self,
                 redirection_type,  # one of REDIRECTION_TYPES
                 output_stream,  # : Text  # destination (string value)
                 input_stream=None  # optional, a stream which is redirected
                 ):
        self.redirection_type = redirection_type
        self.output_stream = self._parse_output_stream(output_stream)
        self.input_stream = self._parse_input_stream(input_stream)

    def __del__(self):
        standard_streams = list(
            Redirection.STANDARD_STREAMS.keys()
            ) + list(
            Redirection.STANDARD_FILES.keys()
        )

        for stream in (self.output_stream, self.input_stream):
            # Do not clear standard streams
            if str(stream.fileno()) in standard_streams:
                continue
            stream.close()

    def _parse_stream(self,
                      stream_name  # : Text
                      ):
        """Determines a stream from string value"""

        if stream_name in Redirection.STANDARD_FILES:
            return Redirection.STANDARD_FILES[stream_name]

        if stream_name in Redirection.STANDARD_STREAMS:
            return Redirection.STANDARD_STREAMS[stream_name]

        # Check value for representing custom file descriptors
        pattern = re.search(r"&(\d+)", stream_name)

        if pattern:
            return os.fdopen(
                fd=int(pattern.group(1)),
                mode=REDIRECTION_MODES[self.redirection_type]
            )

        # Any regular file
        return open(
            file=stream_name,
            mode=REDIRECTION_MODES[self.redirection_type]
        )

    def _parse_output_stream(self,
                             output_stream  # : Text
                             ):

        return self._parse_stream(output_stream)

    def _parse_input_stream(self,
                            input_stream  # : Text
                            ):
        if input_stream is None:
            input_stream = self.DEFAULT_OUTPUT_STREAM

        return self._parse_stream(input_stream)
