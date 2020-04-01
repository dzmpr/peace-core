from src.syntaxer.Phrase import Phrase, PhraseClass


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

    def process_phrase(self, phrase: Phrase):
        # Scope block opens
        if phrase.phrase_class == PhraseClass.body or phrase.phrase_class == PhraseClass.expression or phrase.phrase_class == PhraseClass.device:
            self.braceCount = self.braceCount + 1

        # Scope block closes
        elif phrase.phrase_class == PhraseClass.blockClose:
            self.braceCount = self.braceCount - 1

        # Check label name
        elif phrase.phrase_class == PhraseClass.label:
            if phrase.params[0].value not in self.entries:
                self.entries[phrase.params[0].value] = phrase.phrase_class
            else:
                raise SyntaxParseError("Name \"{}\" already taken by {}.".format(phrase.params[0].value,
                                                                                 self.entries[phrase.params[0].value]))

        # Check name
        elif phrase.phrase_class == PhraseClass.operator:
            pass
        # TODO: process operator
