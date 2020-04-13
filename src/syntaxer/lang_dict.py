from typing import Dict, List, Union
from enum import Enum
from lexer.token import TokenClass


class SignatureType(Enum):
    operator = 0
    expression = 1


class Signature:
    def __init__(self,
                 signature_type: SignatureType,
                 output: str,
                 req_params: int,
                 max_params: int,
                 params: List[TokenClass]):
        self.signature_type = signature_type
        self.output = output
        self.req_params = req_params
        self.max_params = max_params
        self.params = params


class LangDict:
    def __init__(self):
        self.ld: Dict[str, Signature] = dict()

    def add_word(self,
                 definition: str,
                 signature_type: SignatureType,
                 output: str,
                 req_params: int,
                 params: Union[List[TokenClass], None] = None):
        if params is None:
            params = list()
        self.ld[definition] = Signature(signature_type, output, req_params, len(params), params)

    def get_signature(self, definition: str) -> Signature:
        return self.ld[definition]

    def check_definition(self, definition: str) -> bool:
        if definition in self.ld:
            return True
        return False

    def set_output(self, definition: str, output: str):
        self.ld[definition].output = output
