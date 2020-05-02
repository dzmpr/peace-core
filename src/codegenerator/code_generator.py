from codegenerator.line_composer import LineComposer
from syntaxer.phrase import Phrase, PhraseClass, PhraseSubclass
from syntaxer.lang_dict import LangDict
from parsetree.parse_tree import ParseTree, TreeTraverse, Node
from lexer.token import Token
from typing import TextIO, Callable, Union, List


class CodeGenerator:
    def __init__(self,
                 tree: ParseTree,
                 lang_dict: LangDict,
                 file: TextIO,
                 params: Union[List[Token], None] = None,
                 uses_num: int = 0):
        self._tree: ParseTree = tree
        self._lang_dict: LangDict = lang_dict
        self.composer = LineComposer(lang_dict, self.expression_processor, params, uses_num)
        self._output: TextIO = file
        self._temp_expression: str = ""
        self._write: Callable[[str], None] = self.write_to_file
        self._params = params
        self._stack = list()

    def __repr__(self):
        return f"CG - ({repr(self._tree)}, {repr(self._lang_dict)})"

    def write_to_file(self, line: str):
        self._output.write(line)

    def write_to_str(self, line: str):
        self._temp_expression += line

    def expression_processor(self, definition: str, params: Union[List[Token], None] = None):
        candidates = self._lang_dict.get_candidates(definition)
        expr_signature = self._lang_dict.get_signature(candidates[0])
        expr_generator = CodeGenerator(self._tree, self._lang_dict, self._output, params, expr_signature.uses_number)
        expr_signature.set_output(expr_generator.generate_expression(definition))
        expr_signature.add_use()

    # Callback for processing phrases
    def phrase_processor(self, phrase: Phrase):
        if phrase.phrase_class == PhraseClass.label:
            self.composer.add_label(phrase)
        else:

            if phrase.phrase_subclass == PhraseSubclass.body or phrase.phrase_subclass == PhraseSubclass.device:
                self._stack.append(self.composer.block_open(phrase))
            elif phrase.phrase_class == PhraseClass.operator:
                self.composer.compose_line(phrase)
            elif phrase.phrase_subclass == PhraseSubclass.expression:
                self._stack.append("")
            elif phrase.phrase_class == PhraseClass.comment:
                return
            self._write(self.composer.get_line())
            self.composer.reset_content()

    # Callback for processing subtree leave
    def ascent(self):
        self._write(self._stack.pop())

    def generate_expression(self, expr_name: str) -> str:
        self._write = self.write_to_str
        nodes = self._tree.get_head().nodes
        for node in nodes:
            if node.data.phrase_class == PhraseClass.block:
                if node.data.keyword.value == expr_name:
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
