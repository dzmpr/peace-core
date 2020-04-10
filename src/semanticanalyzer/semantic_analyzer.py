from parsetree.parse_tree import ParseTree
from semanticanalyzer.symbol_table import SymbolTable
from syntaxer.phrase import Phrase, PhraseClass


class SemanticError(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class SemanticAnalyzer:
    def __init__(self, tree: ParseTree, symbol_table: SymbolTable):
        self.tree: ParseTree = tree
        self.table: SymbolTable = symbol_table

    # TODO: First version (without scope-dependent check), to be refactored
    def process_phrase(self, phrase: Phrase):
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
