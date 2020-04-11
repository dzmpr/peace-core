from parsetree.parse_tree import ParseTree
from semanticanalyzer.symbol_table import SymbolTable
from syntaxer.phrase import Phrase, PhraseClass
from lexer.token import TokenClass


class SemanticError(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class SemanticAnalyzer:
    def __init__(self, tree: ParseTree, symbol_table: SymbolTable):
        self.tree: ParseTree = tree
        self.table: SymbolTable = symbol_table

    def process_phrase(self, phrase: Phrase):
        self._name_processing(phrase)
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
            identifier: str = phrase.params[0].value[1:-1]
            if operator == "q":
                if not self.table.is_symbol_presence(identifier):
                    self.table.add_symbol(identifier, phrase.phrase_class)
                else:
                    raise SemanticError(f"Naming error. Name \"{identifier}\" already used by {self.table.get_symbol(identifier).phrase_class.name}.")
            elif operator == "dq":
                if not self.table.is_symbol_presence(identifier):
                    raise SemanticError(f"Name \"{identifier}\" was never defined.")

    def _argument_check(self, phrase: Phrase):
        if phrase.phrase_class == PhraseClass.operator:
            if phrase.keyword.value == "q" or phrase.keyword.value == "dq":
                if phrase.params[0].token_class != TokenClass.word:
                    raise SemanticError(f"Wrong argument for {phrase.phrase_class.name}, expected word.")

            if len(phrase.params) > 1:
                raise SemanticError(f"Found operator with {len(phrase.params)} arguments, but expected 1.")
