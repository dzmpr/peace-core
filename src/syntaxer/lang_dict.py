from typing import Dict, List, Union
from enum import Enum
from lexer.token import TokenClass


class SignatureType(Enum):
    operator = 0
    expression = 1


class Signature:
    def __init__(self, signature_type: SignatureType, output: str, required_params: int, params: Union[List[TokenClass], None] = None):
        self.signature_type = signature_type
        self.output = output
        self.required_params = required_params
        self.params = params


class LangDict:
    def __init__(self):
        self.ld: Dict[str, Signature] = dict()

    def add_word(self,
                 definition: str,
                 signature_type: SignatureType,
                 output: str,
                 required_params: int,
                 params: Union[List[TokenClass], None] = None):
        self.ld[definition] = Signature(signature_type, output, required_params, params)

    def get_signature(self, definition: str) -> Signature:
        return self.ld[definition]

    def check_definition(self, definition: str) -> bool:
        if definition in self.ld:
            return True
        return False

    def set_output(self, definition: str, output: str):
        self.ld[definition].output = output
