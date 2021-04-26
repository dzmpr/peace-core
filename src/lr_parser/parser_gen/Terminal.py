from lr_parser.parser_gen.ProductionItem import ProductionItem, ProductionItemType


class Terminal(ProductionItem):
    EPSILON = "eps"
    EOF = "end_of_file"

    def __init__(self, name: str):
        super().__init__(name, ProductionItemType.TERMINAL_TYPE)

    def __repr__(self):
        return self.item_name

    @classmethod
    def set_eof_output(cls, eof_output: str):
        cls.EOF = eof_output

    @classmethod
    def set_epsilon_output(cls, epsilon_output: str):
        cls.EPSILON = epsilon_output

    @staticmethod
    def get_epsilon():
        return Terminal(Terminal.EPSILON)

    @staticmethod
    def get_eof():
        return Terminal(Terminal.EOF)
