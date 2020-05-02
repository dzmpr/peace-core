from parsetree.parse_tree import ParseTree
from syntaxer.phrase import Phrase, PhraseClass
from syntaxer.interpretation_error import InterpretationError, ErrorType, PeaceError


class TreeComposer:
    def __init__(self, tree: ParseTree):
        """
        Tree composer constructor.

        :param tree: pointer to tree to build
        """
        self._tree: ParseTree = tree

    def __repr__(self):
        return f"Composer node: {self._tree.head.data}"

    def is_tree_valid(self) -> bool:
        """
        Checks if head pointer was returned to root.

        :return: true if head pointer equal to root
        """
        if self._tree.head.parent is None:
            return True
        return False

    def add_phrase(self, phrase: Phrase, phrase_line: int):
        """
        Add new phrase to tree.

        :param phrase: phrase to add
        :param phrase_line: phrase start line
        """
        if phrase.phrase_class == PhraseClass.blockClose:
            if self._tree.head.parent is not None:
                self._tree.ascend()
            else:
                raise InterpretationError(
                    PeaceError(f"Extra '}}' was found.",
                               ErrorType.syntax_error, phrase_line))
            return
        self._tree.add_leaf(phrase)
        if phrase.phrase_class == PhraseClass.block:
            self._tree.submerge()
