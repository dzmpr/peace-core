from codegenerator.line_composer import LineComposer
from syntaxer.phrase import Phrase, PhraseClass, PhraseSubclass
from syntaxer.lang_dict import LangDict
from parsetree.parse_tree import ParseTree, TreeTraverse, Node
from typing import TextIO, Callable


class CodeGenerator:
    def __init__(self, tree: ParseTree, lang_dict: LangDict, file: TextIO):
        self._tree: ParseTree = tree
        self._lang_dict: LangDict = lang_dict
        self.lc = LineComposer(lang_dict)
        self._output: TextIO = file
        self._temp_expression: str = ""
        self._write: Callable[[str], None] = self.write_to_file
        self._stack = list()

    def __repr__(self):
        return f"CG - ({repr(self._tree)}, {repr(self._lang_dict)})"

    def write_to_file(self, line: str):
        self._output.write(line)

    def write_to_str(self, line: str):
        self._temp_expression += line

    def phrase_processor(self, phrase: Phrase):
        if phrase.phrase_class == PhraseClass.label:
            self.lc.add_label(phrase)
        else:
            if phrase.phrase_subclass == PhraseSubclass.body or phrase.phrase_subclass == PhraseSubclass.device:
                self._stack.append(self.lc.block_open(phrase))
            elif phrase.phrase_class == PhraseClass.operator:
                self.lc.compose_line(phrase)
            elif phrase.phrase_subclass == PhraseSubclass.expression:
                self._stack.append("")
            elif phrase.phrase_class == PhraseClass.comment:
                return
            self._write(self.lc.get_line())
            self.lc.reset_content()

    def ascent(self):
        self._write(self._stack.pop())

    def generate_expression(self, node) -> str:
        self._write = self.write_to_str
        tree_traverse = TreeTraverse(node, self.phrase_processor, self.ascent)
        tree_traverse.traverse()
        return self._temp_expression

    def generate(self, node: Node):
        self._write = self.write_to_file
        tree_traverse = TreeTraverse(node, self.phrase_processor, self.ascent)
        tree_traverse.traverse()

    def compile(self):
        blocks = self._tree.get_head().nodes
        for node in blocks:
            if node.data.phrase_subclass == PhraseSubclass.body:
                self.generate(node)
            elif node.data.phrase_subclass == PhraseSubclass.expression:
                self._lang_dict.set_output(node.data.keyword.value, self.generate_expression(node))
                self._temp_expression = ""
            elif node.data.phrase_class == PhraseClass.comment:
                continue
