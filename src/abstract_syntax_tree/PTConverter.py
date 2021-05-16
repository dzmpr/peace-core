from typing import Optional

from parsetree.parse_tree import ParseTree
from semanticanalyzer.semantic_analyzer import SemanticAnalyzer
from semanticanalyzer.symbol_table import SymbolTable
from slr_parser.ParseTreeNode import ParseTreeNode
from syntaxer.lang_dict import LangDict
from syntaxer.phrase import PhraseClass
from slr_parser.phrase_builder import phrase_builder


class PTConverter:
    def __init__(self, output_tree: ParseTree, symbol_table: SymbolTable, lang_dict: LangDict):
        self.parse_tree_head: Optional[ParseTreeNode] = None
        self.output_tree: ParseTree = output_tree
        self.semantic_analyzer = SemanticAnalyzer(output_tree, symbol_table, lang_dict)
        self._stack: list = list()
        self._node_stack: list[ParseTreeNode] = list()
        self._index: int = 0
        self._temp: Optional[ParseTreeNode] = None

    def convert_pt(self, parse_tree: ParseTreeNode):
        current_node = parse_tree
        while True:
            try:
                self._temp = current_node[self._index]

            except IndexError:
                if len(self._stack):
                    if current_node.name == "Block" or current_node.name == "Program":
                        self.semantic_analyzer.ascend()
                    self._index = self._stack.pop()
                    current_node = self._node_stack.pop()
                else:
                    break

            else:
                self._index += 1
                self.process_node(self._temp)
                if len(self._temp.child_nodes):
                    self._stack.append(self._index)
                    self._node_stack.append(current_node)
                    current_node = self._temp
                    self._index = 0

    # def convert_to_ast(self) -> ProgramNode:
    #     ast_head = ProgramNode()
    #     current_node = self.parse_tree_head
    #     while False:
    #         ...
    #     return ast_head

    def process_node(self, current_node: ParseTreeNode):
        phrase_class = self.get_phrase_class(current_node.name)
        phrase = phrase_builder(self.output_tree.get_context(), phrase_class, current_node)
        if phrase:
            self.semantic_analyzer.process_phrase(phrase, -1)

    @staticmethod
    def get_phrase_class(name: str) -> PhraseClass:
        if name == "Block":
            return PhraseClass.block
        elif name == "Label":
            return PhraseClass.label
        elif name == "Operator":
            return PhraseClass.operator
