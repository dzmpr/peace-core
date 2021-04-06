from enum import Enum


class ProductionItemType(Enum):
    TERMINAL_TYPE = 0
    NONTERMINAL_TYPE = 1


class ProductionItem:
    def __init__(self, item_name: str, item_type: ProductionItemType):
        self.item_name: str = item_name
        self.item_type: ProductionItemType = item_type

    def __hash__(self) -> int:
        return hash((self.item_name, self.item_type))

    def __eq__(self, other):
        if isinstance(other, ProductionItem):
            return self.item_name == other.item_name and self.item_type == other.item_type
        return False

    def is_terminal(self) -> bool:
        return self.item_type == ProductionItemType.TERMINAL_TYPE

    def is_nonterminal(self) -> bool:
        return self.item_type == ProductionItemType.NONTERMINAL_TYPE
