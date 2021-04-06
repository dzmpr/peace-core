from lr_parser.parser_gen.ProductionItem import ProductionItem, ProductionItemType


class Terminal(ProductionItem):
    def __init__(self, name: str):
        super().__init__(name, ProductionItemType.TERMINAL_TYPE)

    def __repr__(self):
        return self.item_name
