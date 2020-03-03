from src.syntaxer.rules import operators
from src.syntaxer.SyntaxerStateMachine import Phrase


class BlockStack:
    def __init__(self):
        self.blocks = []

    def push(self, item):
        self.blocks.append(item)

    def pop(self):
        return self.blocks.pop()

    def isempty(self):
        return self.blocks == []



class CodeGenerator:
    def __init__(self):
        self.template = " {:7} {:9} {:<}\n"
        self.keyword = ""
        self.parameters = ""
        self.label = ""
        self.stack = BlockStack()
        self.line = ""

    def getLine(self):
        return self.line

    def generateLine(self, phrase):
        line = self.template
        self.keyword = operators[phrase[1][0][1]]
        self.parameters = phrase[1][1][1][1:-1]
        self.line = line.format(self.label, self.keyword, self.parameters)

    def resetContent(self):
        self.keyword = ""
        self.parameters = ""
        self.label = ""

    def addLabel(self, phrase):
        self.label = phrase[1][0][1]

    def blockOpen(self, phrase):
        open = self.template
        close = self.template
        if phrase[0] == Phrase.body:
            self.keyword = "SIMULATE"
            open = open.format(self.label, self.keyword, self.parameters)
            self.keyword = "END"
            close = close.format(self.label, self.keyword, self.parameters)
            self.stack.push(close)
        else:
            self.keyword = "SEIZE"
            self.parameters = phrase[1][0][1]
            open = open.format(self.label, self.keyword, self.parameters)
            self.keyword = "RELEASE"
            close = close.format(self.label, self.keyword, self.parameters)
            self.stack.push(close)
        self.line = open

    def closeBlock(self, phrase):
        self.line = self.stack.pop()