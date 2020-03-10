from src.syntaxer.SyntaxerStateMachine import PhraseGroup


class SyntaxParseError(Exception):
    def __init__(self, msg):
        self.msg = msg


class SemanticProcessor:
    def __init__(self):
        self.line = 1
        self.braceCount = 0
        self.entries = dict()

    def next_line(self):
        self.line = self.line + 1

    def processed_lines(self):
        return self.line

    def is_block_closed(self):
        if self.braceCount == 0:
            return True
        return False

    def process_phrase(self, phrase):
        # Scope block opens
        if phrase[0] == PhraseGroup.body or phrase[0] == PhraseGroup.expression or phrase[0] == PhraseGroup.device:
            self.braceCount = self.braceCount + 1

        # Scope block closes
        elif phrase[0] == PhraseGroup.blockClose:
            self.braceCount = self.braceCount - 1

        # Check label name
        elif phrase[0] == PhraseGroup.label:
            if phrase[1][0].value not in self.entries:
                self.entries[phrase[1][0].value] = phrase[0]
            else:
                raise SyntaxParseError("Name \"{}\" already taken by {}.".format(phrase[1][0].value, self.entries[phrase[1][0].value]))

        # Check name
        elif phrase[0] == PhraseGroup.operator:
            pass
        # TODO: process operator