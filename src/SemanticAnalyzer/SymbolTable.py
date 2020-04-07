from typing import Dict
from syntaxer.Phrase import PhraseClass


class Symbol:
    def __init__(self, phrase_class: PhraseClass):
        self.phrase_class: PhraseClass = phrase_class


class SymbolTable:
    def __init__(self):
        self._table: Dict[str, Symbol] = dict()

    def is_symbol_presence(self, identifier: str):
        if identifier in self._table:
            return True
        return False

    def is_symbol_equal(self, identifier: str, phrase_class: PhraseClass):
        if self._table[identifier].phrase_class == phrase_class:
            return True
        return False

    def get_symbol(self, identifier: str):
        return self._table[identifier]

    def add_symbol(self, identifier: str, phrase_class: PhraseClass):
        self._table[identifier] = Symbol(phrase_class)
