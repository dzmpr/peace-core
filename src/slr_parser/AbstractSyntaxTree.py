class ASTNode:
    def __init__(self, name: str, childs: list):
        self.name = name
        self.childs = childs

    def __repr__(self):
        return self.name
