from syntaxer.phrase import Phrase, PhraseSubclass
from syntaxer.lang_dict import LangDict, SignatureType
from lexer.token import Token, TokenClass
from typing import List


templates = {
    "regular": " {:6} {:11} {:<}\n",
    "compare": " {:6} TEST {:6} {:<}\n"
}


def parameter_composer(params: List[Token], skip: int = 0) -> str:
    index = skip
    if params[index].token_class == TokenClass.string:
        result = params[index].value[1:-1]
    else:
        result = params[index].value
    index += 1
    while index < len(params):
        result += ","
        if params[index].token_class == TokenClass.string:
            result += params[index].value[1:-1]
        else:
            result += params[index].value
        index += 1
    return result


class LineComposer:
    def __init__(self, lang_dict: LangDict):
        self.lang_dict = lang_dict
        self.keyword: str = ""
        self.parameters: str = ""
        self.label: str = ""
        self.stack = list()
        self.line: str = ""

    def __repr__(self):
        return f"l: {self.label}, k: {self.keyword}, p: {self.parameters}"

    def get_line(self) -> str:
        return self.line

    def compose_line(self, phrase: Phrase):
        phrase_signature = self.lang_dict.get_signature(phrase.keyword.value)
        if phrase_signature.signature_type == SignatureType.operator:
            if phrase.keyword.value != "compare":
                line = templates["regular"]
                if len(phrase.params):
                    self.parameters = parameter_composer(phrase.params)
                self.keyword = phrase_signature.output
            else:
                line = templates["compare"]
                self.parameters = parameter_composer(phrase.params, 1)
                self.keyword = phrase.params[0].value
            self.line = line.format(self.label, self.keyword, self.parameters)
        elif phrase_signature.signature_type == SignatureType.expression:
            self.line = phrase_signature.output

    def reset_content(self):
        self.keyword = ""
        self.parameters = ""
        self.label = ""

    def add_label(self, phrase: Phrase):
        self.label = phrase.keyword.value

    def block_open(self, phrase: Phrase):
        block_open = templates["regular"]
        block_close = templates["regular"]
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
