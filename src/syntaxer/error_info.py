import sys
from syntaxer.syntaxer import SyntaxParseError
from semanticanalyzer.semantic_analyzer import SemanticError
from syntaxer.phrase_builder import PhraseBuildError


def highlight_line(line: str, highlight=None):
    # Add newline if it's last line
    if line.endswith("\n"):
        print(line, end="", file=sys.stderr)
    else:
        print(line, file=sys.stderr)
    # Highlight all line if string not passed
    if highlight is not None:
        index: int = line.find(highlight)
        print(" " * index, end="", file=sys.stderr)
        print("^" * len(highlight), file=sys.stderr)
    else:
        print("^" * len(line), file=sys.stderr)


def get_n_line(n: int, path: str) -> str:
    file = open(path, mode="r", encoding="utf8")
    for i, line in enumerate(file, start=1):
        if i == n:
            file.close()
            return line


def print_error_info(error: Exception, source_path):
    try:
        raise error
    except SyntaxParseError as error:
        parse_error(error, source_path)
    except SemanticError as error:
        semantic_error(error, source_path)
    except PhraseBuildError as error:
        phrase_build_error(error, source_path)


def parse_error(error: SyntaxParseError, source_path: str):
    print(error.msg, file=sys.stderr)
    if error.line is not None:
        line = get_n_line(error.line, source_path)
        if error.token is not None:
            highlight_line(line, error.token.value)
        else:
            highlight_line(line)


def semantic_error(error: SemanticError, source_path: str):
    print(error.msg, file=sys.stderr)
    if error.line is not None:
        line = get_n_line(error.line, source_path)
        if error.identifier is not None:
            highlight_line(line, error.identifier)
        else:
            highlight_line(line)


def phrase_build_error(error: PhraseBuildError, source_path: str):
    print(error.msg, file=sys.stderr)
    if error.line is not None:
        highlight_line(get_n_line(error.line, source_path))
