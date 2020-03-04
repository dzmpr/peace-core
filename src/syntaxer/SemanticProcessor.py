from src.syntaxer.SyntaxerStateMachine import Phrase


class SyntaxParseError(Exception):
    def __init__(self, msg):
        self.msg = msg


class SemanticProcessor:
    def __init__(self):
        self.line = 1
        self.braceCount = 0
        self.entries = dict()

    def nextLine(self):
        self.line = self.line + 1

    def procesedLines(self):
        return self.line

    def isBlocksClosed(self):
        if self.braceCount == 0:
            return True
        return False

    def processPhrase(self, phrase):
        # Scope block opens
        if phrase[0] == Phrase.body or phrase[0] == Phrase.expression or phrase[0] == Phrase.device:
            self.braceCount = self.braceCount + 1
        # Scope block closes
        elif phrase[0] == Phrase.blockClose:
            self.braceCount = self.braceCount - 1
        # Check label name
        elif phrase[0] == Phrase.label:
            if phrase[1][0][1] not in self.entries:
                self.entries[phrase[1][0][1]] = phrase[0]
            elif self.entries[phrase[1][0][1]] != phrase[0]:
                raise SyntaxParseError("Name {} already taken by {}.".format(phrase[1][0][1], self.entries[phrase[1][0][1]]))
        # Check name
        elif phrase[0] == Phrase.operator:
            pass
        # TODO: process operator