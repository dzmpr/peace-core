from typing import Dict, List, Union
from enum import Enum
from lexer.token import TokenClass


class SigType(Enum):
    operator = 0
    expression = 1


class Signature:
    def __init__(self, signature_type: SigType, target: str, params: Union[List[TokenClass], None] = None):
        self.signature_type = signature_type
        self.target = target
        self.params = params


class LangDict:
    def __init__(self):
        self.ld: Dict[str, Signature] = dict()

    def add_word(self,
                 definition: str,
                 signature_type: SigType,
                 target: str,
                 params: Union[List[TokenClass], None] = None):
        self.ld[definition] = Signature(signature_type, target, params)

    def get_signature(self, definition: str) -> Signature:
        return self.ld[definition]

    def check_definition(self, definition: str) -> bool:
        if definition in self.ld:
            return True
        return False
