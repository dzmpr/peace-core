from parsetree.parse_tree import ParseTree
from semanticanalyzer.symbol_table import SymbolTable
from syntaxer.phrase import Phrase, PhraseClass, PhraseSubclass
from syntaxer.lang_dict import LangDict, SignatureType
from lexer.token import TokenClass


class SemanticError(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class SemanticAnalyzer:
    def __init__(self, tree: ParseTree, symbol_table: SymbolTable, lang_dict: LangDict):
        self.tree: ParseTree = tree
        self.table: SymbolTable = symbol_table
        self.lang_dict: LangDict = lang_dict

    def process_phrase(self, phrase: Phrase):
        self._name_processing(phrase)
        self._signature_recorder(phrase)
        self._argument_check(phrase)

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
                                raise SemanticError(f"Naming error. Name \"{identifier}\" already used by {self.table.get_symbol(identifier).phrase_class.name}.")
                        elif operator == "dq":
                            if not self.table.is_symbol_presence(identifier):
                                raise SemanticError(f"Name \"{identifier}\" was never defined.")
            else:
                raise SemanticError(f"Unknown operator \"{operator}\".")

    def _argument_check(self, phrase: Phrase):
        if phrase.phrase_class == PhraseClass.operator:
            keyword = phrase.keyword.value
            param_num = len(phrase.params)
            if keyword == "q" or keyword == "dq":
                if param_num:
                    if phrase.params[0].token_class != TokenClass.word:
                        raise SemanticError(f"Wrong argument for \"{keyword}\", expected word.")
                else:
                    raise SemanticError(f"Found \"{keyword}\" operator with {param_num} arguments, but expected 1.")

            elif keyword == "init":
                if param_num and param_num < 2:
                    if phrase.params[0].token_class != TokenClass.num:
                        raise SemanticError(f"Wrong argument for \"{keyword}\", expected number.")
                else:
                    raise SemanticError(f"Found \"{keyword}\" operator with {param_num} arguments, but expected 1.")

            elif keyword == "destroy":
                if param_num < 2:
                    if param_num:
                        if phrase.params[0].token_class != TokenClass.num:
                            raise SemanticError(f"Wrong argument for \"{keyword}\", expected number.")
                else:
                    raise SemanticError(f"Found \"{keyword}\" operator with {param_num} arguments, but expected 0-1.")

            elif keyword == "delay":
                if param_num and param_num < 3:
                    for param in phrase.params:
                        if param.token_class != TokenClass.num:
                            raise SemanticError(f"Wrong argument for \"{keyword}\", expected number.")
                else:
                    raise SemanticError(f"Found \"{keyword}\" operator with {param_num} arguments, but expected 1-2.")

            elif keyword == "compare":
                if param_num == 2:
                    if phrase.params[0].token_class != TokenClass.word:
                        raise SemanticError(f"Wrong argument for \"{keyword}\", expected word.")
                    if phrase.params[1].token_class != TokenClass.string:
                        raise SemanticError(f"Wrong argument for \"{keyword}\", expected string.")
                else:
                    raise SemanticError(f"Found \"{keyword}\" operator with {param_num} arguments, but expected 2.")

            elif param_num > 1:
                raise SemanticError(f"Found \"{keyword}\" operator with {param_num} arguments, but expected 1.")

    def _signature_recorder(self, phrase: Phrase):
        if phrase.phrase_subclass == PhraseSubclass.expression:
            self.lang_dict.add_word(phrase.keyword.value, SignatureType.expression, "")
