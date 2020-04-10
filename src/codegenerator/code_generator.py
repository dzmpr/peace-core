from codegenerator.line_composer import LineComposer
from syntaxer.phrase import Phrase, PhraseClass, PhraseSubclass
from parsetree.parse_tree import ParseTree, TreeTraverse
from typing import TextIO, Callable


class CodeGenerator:
    def __init__(self, tree: ParseTree, file: TextIO):
        self._tree: ParseTree = tree
        self.lc = LineComposer()
        self._output: TextIO = file
        self._temp_expression: str = ""
        self._write: Callable[[str], None] = self.write_to_file

    def write_to_file(self, line: str):
        self._output.write(line)

    def write_to_str(self, line: str):
        self._temp_expression += line

    def phrase_processor(self, phrase: Phrase):
        if phrase.phrase_class == PhraseClass.label:
            self.lc.add_label(phrase)
        else:
            if phrase.phrase_subclass == PhraseSubclass.body or phrase.phrase_subclass == PhraseSubclass.device:
                self.lc.block_open(phrase)
            elif phrase.phrase_class == PhraseClass.operator:
                self.lc.compose_line(phrase)
            self._write(self.lc.get_line())
            self.lc.reset_content()

    def ascent(self):
        self.lc.close_block()
        self._write(self.lc.get_line())

    def generate_expression(self) -> str:
        self._write = self.write_to_str
        tree_traverse = TreeTraverse(self._tree.get_head(), self.phrase_processor, self.ascent)
        tree_traverse.traverse()
        return self._temp_expression

    def generate(self):
        self._tree.submerge()
        tree_traverse = TreeTraverse(self._tree.get_head(), self.phrase_processor, self.ascent)
        tree_traverse.traverse()
