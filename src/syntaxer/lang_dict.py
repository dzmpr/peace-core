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
        """
        Signature constructor.

        :param signature_type: signature type
        :param output: destination language output
        :param req_params: number of required params
        :param max_params: max number of params that can be passed to operator
        :param params: list of param types
        """
        self.signature_type = signature_type
        self.output = output
        self.req_params = req_params
        self.max_params = max_params
        self.params = params
        self.uses_number = 0

    def __repr__(self):
        return f"{self.signature_type.name}, params: {self.req_params}-{self.max_params}"


class LangDict:
    def __init__(self):
        self.ld: Dict[str, Signature] = dict()

    def __repr__(self):
        return f"Lang dict ({len(self.ld)})"

    def add_signature(self,
                      definition: str,
                      signature_type: SignatureType,
                      output: str,
                      req_params: int,
                      params: Union[List[TokenClass], None] = None):
        """
        Adds signature to language dictionary.

        :param definition: keyword
        :param signature_type: signature type
        :param output: destination language output
        :param req_params: number of required params
        :param params: list of param types
        """
        if params is None:
            params = list()
        self.ld[definition] = Signature(signature_type, output, req_params, len(params), params)

    def get_signature(self, definition: str) -> Signature:
        """
        Get signature by keyword.

        :param definition: keyword to find
        :return: signature by keyword
        """
        return self.ld[definition]

    def check_definition(self, definition: str) -> bool:
        """
        Check if keyword presence in dictionary.

        :param definition: keyword
        :return: true if keyword in dictionary
        """
        if definition in self.ld:
            return True
        return False

    def set_output(self, definition: str, output: str):
        """
        Set new output to signature by keyword.

        :param definition: keyword
        :param output: new destination language output
        """
        self.ld[definition].output = output

    def update_params(self, definition: str, params: List[TokenClass]):
        """
        Update parameter list of defined signature

        :param definition: keyword
        :param params: new parameters list
        """
        self.ld[definition].req_params = len(params)
        self.ld[definition].max_params = len(params)
        self.ld[definition].params = params

    def add_use(self, definition: str):
        self.ld[definition].uses_number += 1
