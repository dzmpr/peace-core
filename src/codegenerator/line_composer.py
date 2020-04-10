from syntaxer.rules import operators
from syntaxer.phrase import Phrase, PhraseClass, PhraseSubclass


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
        self.keyword = operators[phrase.keyword.value]
        self.parameters = phrase.params[0].value[1:-1]
        self.line = line.format(self.label, self.keyword, self.parameters)

    def reset_content(self):
        self.keyword = ""
        self.parameters = ""
        self.label = ""

    def add_label(self, phrase: Phrase):
        self.label = phrase.keyword.value

    def block_open(self, phrase: Phrase):
        block_open = self.template
        block_close = self.template
        if phrase.phrase_subclass == PhraseSubclass.body:
            self.keyword = "SIMULATE"
            block_open = block_open.format(self.label, self.keyword, self.parameters)
            self.keyword = "END"
            block_close = block_close.format(self.label, self.keyword, self.parameters)
            self.stack.append(block_close)
        elif phrase.phrase_subclass == PhraseSubclass.device:
            self.keyword = "SEIZE"
            self.parameters = phrase.keyword.value
            block_open = block_open.format(self.label, self.keyword, self.parameters)
            self.keyword = "RELEASE"
            block_close = block_close.format(self.label, self.keyword, self.parameters)
            self.stack.append(block_close)
        self.line = block_open

    def close_block(self):
        self.line = self.stack.pop()
