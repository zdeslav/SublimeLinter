import re
from base_linter import BaseLinter, INPUT_METHOD_FILE


CONFIG = {
    'language': 'dart',
    'executable': 'dartanalyzer',
    'lint_args': ['--machine', '{filename}'],
    'test_existence_args': '--version',
    'input_method': INPUT_METHOD_FILE
}


class Linter(BaseLinter):
    MESSAGE_RE = re.compile(r'^(?P<level>\w+)\|(?P<category>\w+)\|(?P<kind>\w+)\|(?P<path>.*)\|(?P<line>\d+)\|(?P<col>\d+)\|(?P<length>\d+)\|(?P<message>.*)')

    def parse_errors(self, view, errors, lines, errorUnderlines, violationUnderlines, warningUnderlines, errorMessages, violationMessages, warningMessages):

        for line in errors.splitlines():
            match = self.MESSAGE_RE.match(line)
            if match:
                level = match.group('level')
                # cat = match.group('category')
                # kind = match.group('kind')
                line, col, span = match.group('line'), match.group('col'), match.group('length')
                lineno = int(line)
                colno = int(col) - 2
                length = int(span)

                message = match.group('message')

                warning = level == 'WARNING'

                if warning:
                    messages = warningMessages
                    underlines = warningUnderlines
                else:
                    messages = errorMessages
                    underlines = errorUnderlines

                self.add_message(lineno, lines, message, messages)
                self.underline_range(view, lineno, colno, underlines, length)
