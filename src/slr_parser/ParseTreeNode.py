from ctypes import Union

from lexer.token import Token


class ParseTreeNode:
    def __init__(self, name: str, attributes: list[Token], child_nodes: list['ParseTreeNode']):
        self.name = name
        self.child_nodes: list[ParseTreeNode] = child_nodes
        self.is_empty: bool = False
        self.attributes: list[Token] = attributes
        if not child_nodes:
            self.is_empty = True
        elif len(child_nodes) == 1 and isinstance(child_nodes[0], ParseTreeNode) and child_nodes[0].is_empty:
            self.is_empty = True

    def __repr__(self):
        return self.name

    def __getitem__(self, item) -> 'ParseTreeNode':
        return self.child_nodes[item]
