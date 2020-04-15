from syntaxer.phrase import Phrase, PhraseClass, PhraseSubclass
from typing import List, Callable, Any, Union


class Node:
    def __init__(self, parent: Union['Node', None], data: Any):
        """
        Node constructor.

        :param parent: pointer to parent node
        :param data: data for node
        """
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

    def __repr__(self):
        return f"Root({len(self.root.nodes)}): {repr(self.root.nodes)}"

    def add_leaf(self, phrase: Phrase):
        """
        Adds leaf to current head position.

        :param phrase: data to store in new node
        """
        self.head.nodes.append(Node(self.head, phrase))

    def ascend(self):
        """
        Move head pointer to parent node of current head.
        """
        self.head = self.head.parent

    def submerge(self, index=-1):
        """
        Move head pointer to one of the child nodes (default - latest).

        :param index: index of child node to submerge
        """
        self.head = self.head.nodes[index]

    def get_context(self) -> PhraseSubclass:
        """
        Find nearest node with "block" class.

        :return: subclass of nearest block class
        """
        current = self.head
        while (current.data.phrase_subclass != PhraseSubclass.program and
               current.data.phrase_subclass != PhraseSubclass.body and
               current.data.phrase_subclass != PhraseSubclass.expression):
            current = current.parent
        return current.data.phrase_subclass

    def get_head(self) -> Node:
        """
        Return head node.

        :return: head node
        """
        return self.head

    def reset_head(self):
        """
        Move head pointer to tree root.
        """
        self.head = self.root


class TreeTraverse:
    def __init__(self,
                 branch_head: Node,
                 node_processor: Callable[[Phrase], None],
                 ascent: Callable[[], None]):
        """
        Tree traverse constructor.

        :param branch_head: set subtree root node to traverse
        :param node_processor: callback to process nodes
        :param ascent: callback to process subtree leave
        """
        self._branch_head: Node = branch_head
        self._ascent: Callable[[], None] = ascent
        self._node_processor: Callable[[Phrase], None] = node_processor
        self._stack: list = list()
        self._index: int = 0
        self._temp: Node = branch_head

    def __repr__(self):
        return f"Traverse node: {self._branch_head}"

    def traverse(self):
        """
        Traverse specified subtree.
        """
        self._node_processor(self._branch_head.data)
        while True:
            try:
                self._temp = self._branch_head[self._index]

            except IndexError:
                self._ascent()
                if len(self._stack):
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
