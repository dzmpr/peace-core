from src.syntaxer.rules import operators


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
        self.line = " {:5} {:11} {:<}\n"
        self.keyword = ""
        self.parameters = ""
        self.label = ""
        self.stack = BlockStack

    def generateLine(self, phrase):
        line = self.line
        self.keyword = operators[phrase[1][0][1]]
        self.parameters = phrase[1][1][1][1:-1]
        return line.format(self.label, self.keyword, self.parameters)

    def resetContent(self):
        self.keyword = ""
        self.parameters = ""
        self.label = ""
