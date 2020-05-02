from enum import Enum
from typing import List, Union
from lexer.token import Token


class PhraseClass(Enum):
    def __repr__(self):
        return self.name

    block = 0
    operator = 1
    comment = 2
    label = 3
    blockClose = 4


class PhraseSubclass(Enum):
    def __repr__(self):
        return self.name

    program = 0
    body = 1
    expression = 2
    device = 3


class Phrase:
    def __init__(self,
                 phrase_class: PhraseClass,
                 phrase_subclass: Union[PhraseSubclass, None] = None,
                 signature_id: Union[int, None] = None,
                 keyword: Union[Token, None] = None,
                 params: Union[List[Token], None] = None):
        self.phrase_class = phrase_class
        self.phrase_subclass = phrase_subclass
        self.signature_id = signature_id
        self.keyword = keyword
        self.params = params

    def __repr__(self):
        if self.phrase_subclass is not None:
            return f"{self.phrase_class.name} ({self.phrase_subclass.name})"
        return f"{self.phrase_class.name}"

    def __str__(self):
        if self.phrase_subclass is not None:
            return f"{self.phrase_class.name} ({self.phrase_subclass.name}), val: {self.params}"
        return f"{self.phrase_class.name}, val: {self.params}"
