from enum import Enum


class ProductionItemType(Enum):
    TERMINAL_TYPE = 0
    NONTERMINAL_TYPE = 1


class ProductionItem:
    def __init__(self, item_name: str, item_type: ProductionItemType):
        self.item_name: str = item_name
        self.item_type: ProductionItemType = item_type
