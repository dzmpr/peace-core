from typing import Dict, List, Union
from enum import Enum
from lexer.token import TokenClass


class SignatureType(Enum):
    operator = 0
    expression = 1


class Signature:
    def __init__(self,
                 signature_type: SignatureType,
                 definition: str,
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
        self.definition = definition
        self.output = output
        self.required_params = req_params
        self.max_params = max_params
        self.params = params
        self.uses_number = 0
        self.contains_param: bool = False

    def __repr__(self):
        return f"{self.signature_type.name}, params: {self.required_params}-{self.max_params}"

    def update_params(self, params: List[TokenClass]):
        """
        Update parameter list of defined signature

        :param params: new parameters list
        """
        self.required_params = len(params)
        self.max_params = len(params)
        self.params = params

    def add_use(self):
        self.uses_number += 1


class LangDict:
    def __init__(self):
        self.ld: Dict[int, Signature] = dict()
        self.counter: int = 0

    def __repr__(self):
        return f"Lang dict ({len(self.ld)})"

    def add_signature(self,
                      definition: str,
                      signature_type: SignatureType,
                      output: str,
                      req_params: int,
                      params: Union[List[TokenClass], None] = None) -> int:
        """
        Adds signature to language dictionary.

        :param definition: keyword
        :param signature_type: signature type
        :param output: destination language output
        :param req_params: number of required params
        :param params: list of param types
        :return identifier of added signature
        """
        if params is None:
            params = list()
        self.ld[self.counter] = Signature(signature_type, definition, output, req_params, len(params), params)
        self.counter += 1
        return self.counter - 1

    def get_candidates(self, definition: str) -> List[int]:
        """
        Get signatures indexes that fits definition.

        :param definition: keyword to find
        :return: list of signatures that fits definition
        """
        result = list()
        for num, signature in self.ld.items():
            if signature.definition == definition:
                result.append(num)
        return result

    def get_signature(self, identifier: int) -> Union[Signature, None]:
        """
        Check if keyword presence in dictionary.

        :param identifier: signature identifier
        :return: signature if it was found, otherwise - None
        """
        return self.ld.get(identifier)
