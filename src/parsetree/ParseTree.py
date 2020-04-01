from src.syntaxer.Phrase import Phrase
from typing import List


class Node:
    def __init__(self, parent: 'Node' or None, phrase: Phrase or None):
        self.parent: Node or None = parent
        self.phrase: Phrase or None = phrase
        self.nodes: List[Node] = list()

    def __getitem__(self, item):
        return self.nodes[item]

    def __repr__(self):
        if self.phrase is None:
            return f"Node ({len(self.nodes)})"
        return f"Node {self.phrase.phrase_class.name} ({len(self.nodes)})"


class ParseTree:
    def __init__(self):
        self.root: Node = Node(None, None)
        self.head: Node = self.root

    def add_leaf(self, phrase: Phrase):
        self.head.nodes.append(Node(self.head, phrase))

    def ascend(self):
        self.head = self.head.parent

    def submerge(self, index=-1):
        self.head = self.head.nodes[index]

    def get_head_class(self):
        if self.head.phrase is not None:
            return self.head.phrase.phrase_class
        return None

    def get_head(self):
        return self.head

    def reset_head(self):
        self.head = self.root
