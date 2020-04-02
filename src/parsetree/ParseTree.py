from src.syntaxer.Phrase import Phrase, PhraseClass
from typing import List, Callable


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

    def get_head_class(self) -> PhraseClass or None:
        if self.head.phrase is not None:
            return self.head.phrase.phrase_class
        return None

    def get_head(self) -> Node:
        return self.head

    def reset_head(self):
        self.head = self.root


class TreeTraverse:
    def __init__(self, tree: Node, node_processor: Callable[[Phrase], None], ascent: Callable[[], None]):
        self._tree: Node = tree
        self._ascent: Callable[[], None] = ascent
        self._node_processor: Callable[[Phrase], None] = node_processor
        self._stack: list = list()
        self._index: int = 0
        self._temp: Node = tree

    def traverse(self):
        self._node_processor(self._tree.phrase)
        while True:
            try:
                self._temp = self._tree[self._index]

            except IndexError:
                self._ascent()
                if len(self._stack):
                    self._index = self._stack.pop()
                    self._tree = self._tree.parent
                else:
                    break

            else:
                self._index += 1
                if len(self._temp.nodes):
                    self._stack.append(self._index)
                    self._tree = self._temp
                    self._index = 0
                else:
                    self._node_processor(self._temp.phrase)
