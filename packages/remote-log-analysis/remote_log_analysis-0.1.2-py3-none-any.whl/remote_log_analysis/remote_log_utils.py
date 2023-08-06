import re
from dataclasses import dataclass
import typing
import copy
import abc
from .remote_file_base import RemoteFileBase


def timestamp_format_to_regex(strftime_notation):
    '''
    :param strftime_notation: A string using strtime notation describing a timestamp format
    :return: A regex which can match the timestamp format
    '''
    special_chars = {
        'Y': r'\d{4}',
        'm': r'\d{2}',
        'd': r'\d{2}',
        'H': r'\d{2}',
        'I': r'\d{2}',
        'M': r'\d{2}',
        'S': r'\d{2}',
        'f': r'\d+',
        'z': r'[+-]\d{4}',
        'Z': r'\w+',
        'a': r'\w{3}',
        'A': r'\w+',
        'b': r'\w{3}',
        'B': r'\w+',
        'c': r'.+',
        'x': r'\d{2}/\d{2}/\d{2}',
        'X': r'\d{2}:\d{2}:\d{2}',
        'p': r'(?:AM|PM)',
        's': r'\d+',
        'w': r'\d',
        'j': r'\d{3}',
        'U': r'\d{2}',
        'W': r'\d{2}',
        'g': r'\d{2}',
        'G': r'\d{4}',
        'V': r'\d{2}',
        '%': r'%'
    }

    chars_to_escape = {'{', '}', '[', ']', '(', ')', '|', '*', '+', '?', '.', '\\', '^', '$'}
    escaped_chars = [re.escape(t) if t in chars_to_escape else t for t in strftime_notation]
    strftime_notation = ''.join(escaped_chars)
    pattern = re.compile(r"(%)(.)")

    def replace_special(match):
        if match.group(1) == '%':
            char = match.group(2)
            if char in special_chars:
                return special_chars[char]
            else:
                return (f'%{char}')
        else:
            raise RuntimeError('Unexpected match while processing timestamp format')

    return pattern.sub(replace_special, strftime_notation)


@dataclass(frozen=True)
class LogLineData:
    timestamp: str
    log_level: str
    source: str
    message: str


class LogLineFormatInterface(metaclass=abc.ABCMeta):
    '''
    Interface for a log line format. The only required method is match which returns
    details about the matched line in a LogLineData object if a match occurs. Text log traversal implementations can
    use this interface to extract details about log lines in a variety of formats.
    '''

    @abc.abstractmethod
    def match(self, line: str) -> typing.Optional[LogLineData]:
        '''
        :param line: A line to match
        :return: A LogLineData object if the line matches the format, None otherwise
        '''
        raise NotImplementedError


class CommonRegexLineFormat(LogLineFormatInterface):
    '''
    Describes the format of a log line. A logline is described with the following tokens:
        %t - Timestamp
        %l - Log level
        %s - Source
        %m - Log message
    Other characters are treated as literals.
    The timestamp is further specified in strftime format in timestamp_format.
    The log levels are specified in log_levels in order of increasing severity.

    This class will work well for most common log line formats where the format of the line can be described with
    a regular expression and the timestamp can be described with strftime notation.

    This should cover the majority of text log formats. A custom formatter can be defined as necessary in the event
    this formatter is insufficient. For convenience, a CommonNonRegexLineFormat is provided for simple cases where
    the log line format is a literal string apart from %t %l %s %m as described above.
    '''

    def __init__(self, logline_format: str, timestamp_format: str, log_levels: typing.Iterable[str]):
        '''
        :param logline_format: Specifies the log line format with the tokens described above:
        %t - Timestamp
        %l - Log level
        %s - Source
        %m - Log message
        Other characters are passed to re.compile directly. Be careful to escape these special character sequences:
        {, }, [, ], (, ), |, *, +, ?, ., \\, ^, $
        Use CommonNonRegexLineFormat if you want to match a literal string.
        :param timestamp_format: The timestamp format in strftime notation. See
        https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes. The formatter will attempt
        to match a pattern but will not validate the timestamp.
        :param log_levels: A list of log levels in order of increasing severity. These are the acceptable values for %l
        '''

        self._logline_format = logline_format
        self._timestamp_format = timestamp_format
        self._log_levels = copy.copy(log_levels)
        self._regex = self._generate_regex(logline_format, timestamp_format, log_levels)

    @property
    def regex(self):
        return self._regex

    @property
    def timestamp_format(self):
        return self._timestamp_format

    @property
    def log_levels(self):
        return self._log_levels

    def match(self, line: str) -> typing.Optional[LogLineData]:
        '''
        :param line: A line from a log file
        :return: A LogLineData object if the line matches the format, otherwise None
        '''
        match_result = self._regex.search(line)
        if not match_result:
            return None

        # source info is not always present.
        match_groups = match_result.groupdict()

        return LogLineData(timestamp=match_groups.get('t', ''),
                           log_level=match_groups.get('l', ''),
                           source=match_groups.get('s', ''),
                           message=match_groups.get('m', ''))

    def _generate_regex(self, logline_format, timestamp_format, log_levels):
        format_chars = {
            't': timestamp_format_to_regex(timestamp_format),
            'l': '(?:' + '|'.join(log_levels) + ')',
            's': r'[^\s]+',
            'm': r'.*',
        }

        regex = re.compile(re.sub(r'%([tlsm])',
                                  lambda x: f'(?P<{x.group(1)}>{format_chars[x.group(1)]})',
                                  logline_format))

        return regex


class CommonNonRegexLineFormat(CommonRegexLineFormat):
    '''
    A convenience class for specifying a literal log line format apart from the special %t %l %s %m tokens.
    '''
    def __init__(self, logline_format: str, timestamp_format: str, log_levels: typing.Iterable[str]):
        '''
        :param logline_format: Specifies the log line format with the tokens described above:
        %t - Timestamp
        %l - Log level
        %s - Source
        %m - Log message
        :param timestamp_format: The timestamp format in strftime notation
        :param log_levels: A list of log levels in order of increasing severity. These are the acceptable values for %l
        '''
        # escape any special sequences in logline_format before proceeding
        chars_to_escape = {'{', '}', '[', ']', '(', ')', '|', '*', '+', '?', '.', '\\', '^', '$'}
        escaped_chars = [re.escape(t) if t in chars_to_escape else t for t in logline_format]
        logline_format = ''.join(escaped_chars)
        super().__init__(logline_format, timestamp_format, log_levels)


class LogLineSplitterInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __iter__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def read(self) -> typing.Optional[LogLineData]:
        raise NotImplementedError

    @abc.abstractmethod
    def clear(self):
        '''
        Clear any state associated with the splitter. The next read will read from the file
        :return:
        '''
        raise NotImplementedError


class UnixLogLineSplitter(LogLineSplitterInterface):
    '''
        Split a block of text into log lines. Log lines are newline separated.
        A line which does not match the format of the specified log line format is considered a continuation of the
        previous line. This base splitter handles files with UNIX style line endings. Sub-class and set
        self._multiline_join to '\r\n' to handle files with Windows style line endings.
    '''

    def __init__(self, reader: RemoteFileBase, log_line_format: LogLineFormatInterface):
        if not reader.text_mode:
            raise RuntimeError('LogLineSplitter requires a text mode reader')

        self._reader = reader
        self._log_line_format = log_line_format
        self._lines = []
        self._current_context = []
        self._match = None
        self._eof = False
        self._multiline_join = '\n'

    def clear(self):
        self._lines = []
        self._current_context = []
        self._match = None
        self._eof = False

    def _handle_return_match(self):
        match = self._match
        self._match = None
        if not match:
            return None

        if self._current_context:
            message = match.message + self._multiline_join + self._multiline_join.join(self._current_context)
            self._current_context = []
            return LogLineData(timestamp=match.timestamp,
                               log_level=match.log_level,
                               source=match.source,
                               message=message)
        else:
            return match

    def __iter__(self):
        while True:
            result = self.read()
            if not result:
                return
            yield result

    def read(self) -> typing.Optional[LogLineData]:
        '''
        Read the next LogLineData from the reader. If the reader is at EOF, return None.
        :return: A LogLineData object if a line was read, None otherwise
        '''
        if self._eof and not (self._lines or self._match):
            return None

        while True:
            if len(self._lines) <= 1:
                if not self._eof:
                    try:
                        self._from_reader()
                    except EOFError:
                        self._eof = True

            if not self._lines:
                return self._handle_return_match()

            line = self._lines[0]
            if not line[0]:
                line[0] = self._log_line_format.match(line[1])
            match = line[0]

            if match and self._match:
                return self._handle_return_match()
            elif match and not self._match:
                self._match = match
                self._lines.pop(0)
            elif not match and self._match:
                self._current_context.append(line[1])
                self._lines.pop(0)
            else:
                # non-matching line and no match in progress
                self._lines.pop(0)

    def _from_reader(self):
        text = self._reader.read().data.splitlines(keepends=True)
        # If the last line does not end with a newline, add one
        if self._lines and self._lines[-1][1][-1] != '\n':
            self._lines[-1][1] += text[0]
            text.pop(0)

        self._lines.extend([None, l] for l in text)


class DosLineSplitter(UnixLogLineSplitter):
    def __init__(self, reader: RemoteFileBase, log_line_format: LogLineFormatInterface):
        super().__init__(reader, log_line_format)
        self._multiline_join = '\r\n'


class LineSplitter(UnixLogLineSplitter):
    def __init__(self, reader: RemoteFileBase, log_line_format: LogLineFormatInterface):
        super().__init__(reader, log_line_format)
        self._line_ending_determined = False

    def read(self) -> typing.Optional[LogLineData]:
        if self._line_ending_determined:
            return super().read()
        else:
            super()._from_reader()
            if self._lines[0][1].find('\r\n') != -1:
                self._multiline_join = '\r\n'
            self._line_ending_determined = True
            return super().read()
