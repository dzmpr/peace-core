import unittest

from parsetree.parse_tree import ParseTree, Node
from syntaxer.phrase import Phrase, PhraseClass, PhraseSubclass
from test_phrase_builder import are_phrases_equal


def are_nodes_equal(node: Node, reference: Node) -> bool:
    def print_difference(place, a, b):
        print(f"Found difference in {place}.")
        print(f"Resulted \"{str(a)}\" isn't equals to expected \"{str(b)}\".")

    # Check data for None
    if node.data is not reference.data:
        # Check is any of nodes has None data
        if node.data is None or reference.data is None:
            print_difference("node data", node.data, reference.data)
            return False
        else:
            # Check is data content equal
            if not are_phrases_equal(node.data, reference.data):
                print_difference("node data", node.data, reference.data)
                return False

    # Check parent for None
    if node.parent is not reference.parent:
        # Check is any of nodes hasn't parent
        if node.parent is not None or reference.parent is not None:
            print_difference("node parent", node.parent, reference.parent)
            return False
        else:
            # Check is parents equal
            if node.parent != reference.parent:
                print_difference("node data", node.parent, reference.parent)
                return False

    if node.nodes != reference.nodes:
        print_difference("nodes", node.nodes, reference.nodes)
        return False
    return True


class TestParseTree(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tree = ParseTree()
        cls.tree.add_leaf(Phrase(PhraseClass.block, PhraseSubclass.expression))
        cls.tree.submerge()

    def test_tree_get_head(self):
        head = self.tree.get_head()
        self.assertTrue(are_nodes_equal(head, self.tree.head))

    def test_add_node(self):
        phrase_in_node = Phrase(PhraseClass.blockClose)
        expected_node = Node(self.tree.get_head(), phrase_in_node)
        self.tree.add_leaf(phrase_in_node)
        self.assertTrue(are_nodes_equal(self.tree.head.nodes[0], expected_node))

    def test_submerge(self):
        node = self.tree.head.nodes[0]
        self.tree.submerge()
        self.assertTrue(are_nodes_equal(self.tree.get_head(), node))

    def test_get_context(self):
        context = Phrase(PhraseClass.block, PhraseSubclass.program)
        self.assertTrue(are_phrases_equal(self.tree.get_context(), context))

    def test_ascend(self):
        node = self.tree.head.parent
        self.tree.ascend()
        self.assertTrue(are_nodes_equal(self.tree.get_head(), node))

    def test_reset_head(self):
        node = self.tree.root
        self.tree.reset_head()
        self.assertTrue(are_nodes_equal(self.tree.get_head(), node))


if __name__ == '__main__':
    unittest.main()
