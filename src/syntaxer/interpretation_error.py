import sys
from enum import Enum
from typing import Union


class ErrorType(Enum):
    def get_error_name(self) -> str:
        return self.value + " error"

    syntax_error = "Syntax"
    phrase_build_error = "Phrase build"
    naming_error = "Naming"
    parameter_error = "Parameter"


class PeaceError(Exception):
    def __init__(self,
                 msg: str,
                 error_type: ErrorType,
                 line: Union[int, None] = None,
                 highlight: Union[str, None] = None):
        self.msg = msg
        self.type = error_type
        self.line = line
        self.highlight = highlight

    def get_exception(self):
        if self.line is not None:
            return f"{self.type.get_error_name()} at line {self.line}.\n{self.msg}"
        return f"{self.type.get_error_name()}.\n{self.msg}"


class InterpretationError(Exception):
    def __init__(self, error: Union[PeaceError, None] = None):
        self.errors = list()
        if error is not None:
            self.errors.append(error)

    def add_error(self, error: PeaceError):
        self.errors.append(error)


def highlight_line(line: str, highlight=None):
    # Add newline if it's last line
    if line.endswith("\n"):
        print(line, end="", file=sys.stderr)
    else:
        print(line, file=sys.stderr)
    # Highlight all line if string not passed
    if highlight is not None:
        index: int = line.find(highlight)
        for i in range(index):
            if line[i] == "\t":
                print("\t", end="", file=sys.stderr)
            else:
                print(" ", end="", file=sys.stderr)
        print("^" * len(highlight), file=sys.stderr)
    else:
        print("^" * len(line), file=sys.stderr)


def get_n_line(n: int, path: str) -> str:
    file = open(path, mode="r", encoding="utf8")
    for i, line in enumerate(file, start=1):
        if i == n:
            file.close()
            return line


def print_error_info(exception: InterpretationError, source_path: str):
    for error in exception.errors:
        print_error(error, source_path)


def print_error(error: PeaceError, source_path: str):
    print(error.get_exception(), file=sys.stderr)
    if error.line is not None:
        line = get_n_line(error.line, source_path)
        highlight_line(line, error.highlight)
    print("", file=sys.stderr)
