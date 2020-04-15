import sys
from syntaxer.syntaxer import SyntaxParseError


def print_error_info(error: Exception, source_path):
    try:
        raise error
    except SyntaxParseError as error:
        parse_error(error, source_path)


def parse_error(error: SyntaxParseError, source_path: str):
    print(error.msg, file=sys.stderr)
    if error.line is not None and error.token is not None:
        source = open(source_path, mode="r", encoding="utf-8")
        for i, line in enumerate(source, start=1):
            if i == error.line:
                print(line, end="", file=sys.stderr)
                index: int = line.find(error.token.value)
                print(" " * index, end="", file=sys.stderr)
                print("^" * len(error.token.value), file=sys.stderr)
                source.close()
                break
