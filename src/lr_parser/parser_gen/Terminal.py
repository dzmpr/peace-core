from lr_parser.parser_gen.ProductionItem import ProductionItem, ProductionItemType


class Terminal(ProductionItem):
    EPSILON = "epsilon"
    EOF = "end_of_file"

    def __init__(self, name: str):
        super().__init__(name, ProductionItemType.TERMINAL_TYPE)

    def __repr__(self):
        return self.item_name

    @staticmethod
    def get_epsilon():
        return Terminal(Terminal.EPSILON)

    @staticmethod
    def get_eof():
        return Terminal(Terminal.EOF)
