from src.syntaxer.rules import operators
from src.syntaxer.SyntaxerStateMachine import PhraseGroup


class BlockStack:
    def __init__(self):
        self.blocks = []

    def push(self, item):
        self.blocks.append(item)

    def pop(self):
        return self.blocks.pop()

    def is_empty(self):
        return self.blocks == []


class CodeGenerator:
    def __init__(self):
        self.template = " {:6} {:11} {:<}\n"
        self.keyword = ""
        self.parameters = ""
        self.label = ""
        self.stack = BlockStack()
        self.line = ""

    def get_line(self):
        return self.line

    def generate_line(self, phrase):
        line = self.template
        self.keyword = operators[phrase[1][0].value]
        self.parameters = phrase[1][1].value[1:-1]
        self.line = line.format(self.label, self.keyword, self.parameters)

    def reset_content(self):
        self.keyword = ""
        self.parameters = ""
        self.label = ""

    def add_label(self, phrase):
        self.label = phrase[1][0].value

    def block_open(self, phrase):
        open = self.template
        close = self.template
        if phrase[0] == PhraseGroup.body:
            self.keyword = "SIMULATE"
            open = open.format(self.label, self.keyword, self.parameters)
            self.keyword = "END"
            close = close.format(self.label, self.keyword, self.parameters)
            self.stack.push(close)
        else:
            self.keyword = "SEIZE"
            self.parameters = phrase[1][0].value
            open = open.format(self.label, self.keyword, self.parameters)
            self.keyword = "RELEASE"
            close = close.format(self.label, self.keyword, self.parameters)
            self.stack.push(close)
        self.line = open

    def close_block(self, phrase):
        self.line = self.stack.pop()
