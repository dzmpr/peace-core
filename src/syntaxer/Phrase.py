from enum import Enum
from typing import List
from lexer.Token import Token


class PhraseClass(Enum):
    def __repr__(self):
        return self.name

    operator = 0
    expression = 1
    comment = 2
    blockClose = 3
    body = 4
    device = 5
    label = 6


class Phrase:
    def __init__(self, phrase_class: PhraseClass, params: List[Token]):
        self.phrase_class = phrase_class
        self.params = params

    def __repr__(self):
        return f"Phrase {self.phrase_class.name}"

    def __str__(self):
        return f"Phrase {self.phrase_class.name}, value: {self.params}"
