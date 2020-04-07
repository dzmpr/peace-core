from parsetree.parse_tree import ParseTree
from syntaxer.phrase import Phrase, PhraseClass
from syntaxer import syntaxer


class TreeComposer:
    def __init__(self, tree: ParseTree):
        self._tree: ParseTree = tree

    def get_tree(self):
        return self._tree

    def is_tree_valid(self):
        if self._tree.head.parent is None:
            return True
        return False

    def add_phrase(self, phrase: Phrase):
        if phrase.phrase_class == PhraseClass.blockClose:
            if self._tree.head.parent is not None:
                self._tree.ascend()
            else:
                raise syntaxer.SyntaxParseError("Extra '}' was found.")
            return
        self._tree.add_leaf(phrase)
        if (phrase.phrase_class == PhraseClass.body or
                phrase.phrase_class == PhraseClass.expression or
                phrase.phrase_class == PhraseClass.device):
            self._tree.submerge()
