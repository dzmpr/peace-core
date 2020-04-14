from parsetree.parse_tree import ParseTree
from semanticanalyzer.symbol_table import SymbolTable
from syntaxer.phrase import Phrase, PhraseClass, PhraseSubclass
from syntaxer.lang_dict import LangDict, SignatureType


class SemanticError(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class SemanticAnalyzer:
    def __init__(self, tree: ParseTree, symbol_table: SymbolTable, lang_dict: LangDict):
        self.tree: ParseTree = tree
        self.table: SymbolTable = symbol_table
        self.lang_dict: LangDict = lang_dict

    def __repr__(self):
        return f"Semantic an. ({self.tree}, {self.table}, {self.lang_dict})"

    def process_phrase(self, phrase: Phrase):
        self._name_processing(phrase)
        self._signature_recorder(phrase)
        self._params_check(phrase)

    # TODO: First version (without scope-dependent check), to be refactored
    def _name_processing(self, phrase: Phrase):
        if phrase.phrase_class == PhraseClass.block:
            identifier: str = phrase.keyword.value
            if not self.table.is_symbol_presence(identifier):
                self.table.add_symbol(identifier, phrase.phrase_subclass)
            else:
                raise SemanticError(f"Naming error. Name \"{identifier}\" already used by {self.table.get_symbol(identifier).phrase_class.name}.")

        elif phrase.phrase_class == PhraseClass.label:
            identifier: str = phrase.keyword.value
            if not self.table.is_symbol_presence(identifier):
                self.table.add_symbol(identifier, phrase.phrase_class)
            else:
                raise SemanticError(f"Naming error. Name \"{identifier}\" already used by {self.table.get_symbol(identifier).phrase_class.name}.")

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
                                raise SemanticError(f"Naming error. Name \"{identifier}\" already used "
                                                    f"by {self.table.get_symbol(identifier).phrase_class.name}.")
                        elif operator == "dq":
                            if not self.table.is_symbol_presence(identifier):
                                raise SemanticError(f"Name \"{identifier}\" was never defined.")
            else:
                raise SemanticError(f"Unknown operator \"{operator}\".")

    def _params_check(self, phrase: Phrase):
        if phrase.phrase_class == PhraseClass.operator:
            keyword = phrase.keyword.value
            op_signature = self.lang_dict.get_signature(keyword)
            params_num = len(phrase.params)
            if op_signature.req_params <= params_num <= op_signature.max_params:
                for i in range(params_num):
                    if phrase.params[i].token_class != op_signature.params[i]:
                        raise SemanticError(f"Wrong parameter for \"{keyword}\", "
                                            f"expected {op_signature.params[i].name} "
                                            f"but found {phrase.params[i].token_class.name}.")
            else:
                raise SemanticError(f"Found \"{keyword}\" operator with {params_num} "
                                    f"parameters, but expected {op_signature.req_params}-{op_signature.max_params}.")

    def _signature_recorder(self, phrase: Phrase):
        if phrase.phrase_subclass == PhraseSubclass.expression:
            self.lang_dict.add_word(phrase.keyword.value, SignatureType.expression, "", 0)
