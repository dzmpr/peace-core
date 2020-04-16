from parsetree.parse_tree import ParseTree
from parsetree.tree_composer import TreeComposer
from semanticanalyzer.symbol_table import SymbolTable
from syntaxer.phrase import Phrase, PhraseClass, PhraseSubclass
from syntaxer.lang_dict import LangDict, SignatureType
from typing import Union


class SemanticError(Exception):
    def __init__(self,
                 msg: str,
                 line: Union[int, None] = None,
                 identifier: Union[str, None] = None):
        self.msg = msg
        self.line = line
        self.identifier = identifier


class SemanticAnalyzer:
    def __init__(self, tree: ParseTree, symbol_table: SymbolTable, lang_dict: LangDict):
        self.tree: ParseTree = tree
        self.composer: TreeComposer = TreeComposer(tree)
        self.table: SymbolTable = symbol_table
        self.lang_dict: LangDict = lang_dict
        self._line_count: int = 1

    def add_line(self):
        self._line_count += 1

    def remove_line(self):
        self._line_count -= 1

    def get_line(self) -> int:
        return self._line_count

    def __repr__(self):
        return f"Semantic an. ({self.tree}, {self.table}, {self.lang_dict})"

    def process_phrase(self, phrase: Phrase, line_number: int):
        self._name_processing(phrase, line_number)
        self._signature_recorder(phrase)
        self._params_check(phrase, line_number)
        self.composer.add_phrase(phrase)

    # TODO: First version (without scope-dependent check), to be refactored
    def _name_processing(self, phrase: Phrase, line_number: int):
        if phrase.phrase_class == PhraseClass.block:
            identifier: str = phrase.keyword.value
            if not self.table.is_symbol_presence(identifier):
                self.table.add_symbol(identifier, phrase.phrase_subclass)
            else:
                raise SemanticError(f"Naming error at line {self._line_count - 1}."
                                    f"\nName \"{identifier}\" already used by "
                                    f"{self.table.get_symbol(identifier).phrase_class.name}.",
                                    line_number, identifier)

        elif phrase.phrase_class == PhraseClass.label:
            identifier: str = phrase.keyword.value
            if not self.table.is_symbol_presence(identifier):
                self.table.add_symbol(identifier, phrase.phrase_class)
            else:
                raise SemanticError(f"Naming error at line {self._line_count - 1}."
                                    f"\nName \"{identifier}\" already used by "
                                    f"{self.table.get_symbol(identifier).phrase_class.name}.",
                                    line_number, identifier)

        elif phrase.phrase_class == PhraseClass.operator:
            operator: str = phrase.keyword.value
            if self.lang_dict.check_definition(operator):
                sig_type = self.lang_dict.get_signature(operator).signature_type
                if sig_type == SignatureType.operator:
                    if len(phrase.params):
                        identifier: str = phrase.params[0].value
                        if operator == "q":
                            if not self.table.is_symbol_presence(identifier):
                                self.table.add_symbol(identifier, phrase.phrase_class)
                            else:
                                raise SemanticError(f"Naming error at line {self._line_count - 1}.\n"
                                                    f"Name \"{identifier}\" already used by "
                                                    f"{self.table.get_symbol(identifier).phrase_class.name}.",
                                                    line_number, identifier)
                        elif operator == "dq":
                            if not self.table.is_symbol_presence(identifier):
                                raise SemanticError(f"Naming error at line {self._line_count - 1}."
                                                    f"\nName \"{identifier}\" was never defined.",
                                                    line_number, identifier)
            else:
                raise SemanticError(f"Naming error at line {self._line_count - 1}.\nUnknown operator \"{operator}\".",
                                    line_number, operator)

    def _params_check(self, phrase: Phrase, line_number: int):
        if phrase.phrase_class == PhraseClass.operator:
            keyword = phrase.keyword.value
            op_signature = self.lang_dict.get_signature(keyword)
            params_num = len(phrase.params)
            if op_signature.req_params <= params_num <= op_signature.max_params:
                for i in range(params_num):
                    if phrase.params[i].token_class != op_signature.params[i]:
                        raise SemanticError(f"Parameter error at line {self._line_count - 1}.\n"
                                            f"Wrong parameter for \"{keyword}\", expected "
                                            f"{op_signature.params[i].name} but found "
                                            f"{phrase.params[i].token_class.name}.",
                                            line_number, phrase.params[i].value)
            else:
                raise SemanticError(f"Parameter error at line {self._line_count - 1}.\n"
                                    f"Found \"{keyword}\" operator with {params_num} "
                                    f"parameters, but expected {op_signature.req_params}-{op_signature.max_params}.",
                                    line_number, keyword)

    def _signature_recorder(self, phrase: Phrase):
        if phrase.phrase_subclass == PhraseSubclass.expression:
            self.lang_dict.add_signature(phrase.keyword.value, SignatureType.expression, "", 0)
