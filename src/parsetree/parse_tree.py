from syntaxer.phrase import Phrase, PhraseClass, PhraseSubclass
from typing import List, Callable, Any


class Node:
    def __init__(self, parent: 'Node' or None, data: Any):
        self.parent: Node or None = parent
        self.data: Any = data
        self.nodes: List[Node] = list()

    def __getitem__(self, item) -> 'Node':
        return self.nodes[item]

    def __repr__(self):
        return f"Node {repr(self.data)} ({len(self.nodes)})"


class ParseTree:
    def __init__(self):
        self.root: Node = Node(None, Phrase(PhraseClass.block, PhraseSubclass.program))
        self.head: Node = self.root

    def add_leaf(self, phrase: Phrase):
        self.head.nodes.append(Node(self.head, phrase))

    def ascend(self):
        self.head = self.head.parent

    def submerge(self, index=-1):
        self.head = self.head.nodes[index]

    def get_context(self) -> PhraseSubclass:
        current = self.head
        while (current.data.phrase_subclass != PhraseSubclass.program and
               current.data.phrase_subclass != PhraseSubclass.body and
               current.data.phrase_subclass != PhraseSubclass.expression):
            current = current.parent
        return current.data.phrase_subclass

    def get_head(self) -> Node:
        return self.head

    def reset_head(self):
        self.head = self.root


class TreeTraverse:
    def __init__(self, branch_head: Node, node_processor: Callable[[Phrase], None], ascent: Callable[[], None]):
        self._branch_head: Node = branch_head
        self._ascent: Callable[[], None] = ascent
        self._node_processor: Callable[[Phrase], None] = node_processor
        self._stack: list = list()
        self._index: int = 0
        self._temp: Node = branch_head

    def traverse(self):
        self._node_processor(self._branch_head.data)
        while True:
            try:
                self._temp = self._branch_head[self._index]

            except IndexError:
                if len(self._stack):
                    self._ascent()
                    self._index = self._stack.pop()
                    self._branch_head = self._branch_head.parent
                else:
                    break

            else:
                self._index += 1
                self._node_processor(self._temp.data)
                if len(self._temp.nodes):
                    self._stack.append(self._index)
                    self._branch_head = self._temp
                    self._index = 0
