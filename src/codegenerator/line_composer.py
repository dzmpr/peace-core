from syntaxer.phrase import Phrase, PhraseSubclass
from syntaxer.lang_dict import LangDict, SignatureType, Signature
from lexer.token import Token, TokenClass
from typing import List, Callable, Union


templates = {
    "regular": " {:6} {:11} {:<}\n",
    "compare": " {:6} TEST {:6} {:<}\n"
}


class LineComposer:
    def __init__(self,
                 lang_dict: LangDict,
                 expr_gen: Callable,
                 param_list: Union[List[Token], None] = None,
                 expr_uses: int = 0):
        self.lang_dict = lang_dict
        self.expr_gen = expr_gen
        self.param_list = param_list
        self.expr_uses = expr_uses
        self.keyword: str = ""
        self.parameters: str = ""
        self.label: str = ""
        self.line: str = ""

    def __repr__(self):
        return f"l: {self.label}, k: {self.keyword}, p: {self.parameters}"

    def get_line(self) -> str:
        return self.line

    def compose_line(self, phrase: Phrase):
        phrase_signature = self.lang_dict.get_signature(phrase.keyword.value)
        if phrase_signature.signature_type == SignatureType.operator:
            self._compose_operator(phrase, phrase_signature)
        elif phrase_signature.signature_type == SignatureType.expression:
            self._compose_expression(phrase, phrase_signature)

    def _compose_operator(self, phrase: Phrase, signature: Signature):
        if phrase.keyword.value != "compare":
            line = templates["regular"]
            if len(phrase.params):
                self.parameters = self._parameter_composer(phrase.params)
            self.keyword = signature.output
        else:
            line = templates["compare"]
            self.parameters = self._parameter_composer(phrase.params, 1)
            self.keyword = phrase.params[0].value
        self.line = line.format(self.label, self.keyword, self.parameters)

    def _compose_expression(self, phrase: Phrase, signature: Signature):
        if signature.output == "" or signature.req_params != 0:
            self.expr_gen(phrase.keyword.value, phrase.params)
        self.line = signature.output

    def reset_content(self):
        self.keyword = ""
        self.parameters = ""
        self.label = ""

    def add_label(self, phrase: Phrase):
        self.label = phrase.keyword.value

    def block_open(self, phrase: Phrase) -> str:
        block_open = templates["regular"]
        block_close = templates["regular"]
        if phrase.phrase_subclass == PhraseSubclass.body:
            self.keyword = "SIMULATE"
            block_open = block_open.format(self.label, self.keyword, self.parameters)
            self.keyword = "END"
        elif phrase.phrase_subclass == PhraseSubclass.device:
            self.keyword = "SEIZE"
            self.parameters = phrase.keyword.value
            block_open = block_open.format(self.label, self.keyword, self.parameters)
            self.keyword = "RELEASE"
        block_close = block_close.format(self.label, self.keyword, self.parameters)
        self.line = block_open
        return block_close

    def _parameter_composer(self, params: List[Token], skip: int = 0) -> str:
        """
        Compose parameters string from phrase.

        :param params: parameters
        :param skip: number of parameters to skip
        :return: composed string
        """
        def get_param(param: Token) -> str:
            if param.token_class == TokenClass.string:
                return param.value[1:-1]
            elif param.token_class == TokenClass.parameter:
                if param.value == "@":
                    return str(self.expr_uses)
                else:
                    param_num = int(param.value[1:]) - 1
                    return get_param(self.param_list[param_num])
            else:
                return param.value

        index = skip
        result = get_param(params[index])
        index += 1

        while index < len(params):
            result += ","
            result += get_param(params[index])
            index += 1

        return result
