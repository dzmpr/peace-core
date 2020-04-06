from src.syntaxer.rules import operators
from src.syntaxer.Phrase import Phrase, PhraseClass


class LineComposer:
    def __init__(self):
        self.template: str = " {:6} {:11} {:<}\n"
        self.keyword: str = ""
        self.parameters: str = ""
        self.label: str = ""
        self.stack = list()
        self.line: str = ""

    def get_line(self) -> str:
        return self.line

    def compose_line(self, phrase: Phrase):
        line = self.template
        self.keyword = operators[phrase.params[0].value]
        self.parameters = phrase.params[1].value[1:-1]
        self.line = line.format(self.label, self.keyword, self.parameters)

    def reset_content(self):
        self.keyword = ""
        self.parameters = ""
        self.label = ""

    def add_label(self, phrase: Phrase):
        self.label = phrase.params[0].value

    def block_open(self, phrase: Phrase):
        block_open = self.template
        block_close = self.template
        if phrase.phrase_class == PhraseClass.body:
            self.keyword = "SIMULATE"
            block_open = block_open.format(self.label, self.keyword, self.parameters)
            self.keyword = "END"
            block_close = block_close.format(self.label, self.keyword, self.parameters)
            self.stack.append(block_close)
        else:
            self.keyword = "SEIZE"
            self.parameters = phrase.params[0].value
            block_open = block_open.format(self.label, self.keyword, self.parameters)
            self.keyword = "RELEASE"
            block_close = block_close.format(self.label, self.keyword, self.parameters)
            self.stack.append(block_close)
        self.line = block_open

    def close_block(self):
        self.line = self.stack.pop()
