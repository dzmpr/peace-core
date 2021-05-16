from abstract_syntax_tree.ASTNode import ASTNode


class BlockNode(ASTNode):
    def __init__(self):
        self.block_name: str = str()
        self.block_tag: bool = False
        self.block_entries: list = list()
