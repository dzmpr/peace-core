from lr_parser.parser_gen.ProductionItem import ProductionItem, ProductionItemType


class NonTerminal(ProductionItem):
    def __init__(self, name: str):
        super().__init__(name, ProductionItemType.NONTERMINAL_TYPE)

    def __repr__(self):
        return self.item_name
