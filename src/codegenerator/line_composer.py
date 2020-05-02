from syntaxer.phrase import Phrase, PhraseSubclass
from syntaxer.lang_dict import LangDict, SignatureType, Signature
from lexer.token import Token, TokenClass
from typing import List, Callable, Union

templates = {
    "regular": " {:6} {:11} {:<}\n",
    "compare": " {:6} TEST {:6} {:<}\n",
    "func": " {:6} {:11} {:<}\n {:<}\n"
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
        phrase_signature = self.lang_dict.get_signature(phrase.signature_id)
        if phrase_signature.signature_type == SignatureType.operator:
            self._compose_operator(phrase, phrase_signature)
        elif phrase_signature.signature_type == SignatureType.expression:
            self._compose_expression(phrase, phrase_signature)

    def _compose_operator(self, phrase: Phrase, signature: Signature):
        if phrase.keyword.value == "compare":
            line = templates["compare"]
            self.parameters = self._parameter_composer(phrase.params, 1)
            self.keyword = phrase.params[0].value
            self.line = line.format(self.label, self.keyword, self.parameters)
        elif phrase.keyword.value == "func":
            line = templates["func"]
            self.line = line.format(phrase.params[0].value, signature.output,
                                    phrase.params[1].value[1:-1], phrase.params[2].value[1:-1])
        else:
            line = templates["regular"]
            if len(phrase.params):
                self.parameters = self._parameter_composer(phrase.params)
            self.keyword = signature.output
            self.line = line.format(self.label, self.keyword, self.parameters)

    def _compose_expression(self, phrase: Phrase, signature: Signature):
        if signature.contains_param or signature.output == "":
            # Create new parameters list to replace parametrised arguments to actual params
            params = list()
            for param in phrase.params:
                # Check is parameter has parameter class
                if param.token_class == TokenClass.parameter:
                    # When parameter value "@" - should be inserted expression occurrence number
                    if param.value == "@":
                        params.append(Token(TokenClass.num, str(self.expr_uses)))
                        break
                    # Otherwise insert parameter from parameters list
                    param_num = int(param.value[1:]) - 1
                    params.append(self.param_list[param_num])
                else:
                    # Else insert a parameter from operator
                    params.append(param)

            self.expr_gen(phrase.keyword.value, params)

        self.line = signature.output

    def reset_content(self):
        self.keyword = ""
        self.parameters = ""
        self.label = ""

    def add_label(self, phrase: Phrase):
        if len(phrase.params):
            self.label = phrase.keyword.value + str(self.expr_uses)
            return
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
            if phrase.params is not None:
                self.parameters = phrase.keyword.value + str(self.expr_uses)
            else:
                self.parameters = phrase.keyword.value
            block_open = block_open.format(self.label, self.keyword, self.parameters)
            self.keyword = "RELEASE"
            self.label = ""
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
