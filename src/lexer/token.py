from enum import Enum


class TokenClass(Enum):
    def __init__(self, token_id: int, token_name: str):
        self.token_id = token_id
        self.token_name = token_name

    def __repr__(self):
        return self.name

    @classmethod
    def from_str(cls, name: str):
        for item in TokenClass:
            if item.token_name == name:
                return item
        return None

    undefined = (0, "undef")    # ?
    word = (1, "word")          # +
    parameter = (2, "param")    # -
    space = (3, "space")        # ?
    num = (4, "num")            # +
    sign = (5, "sign")          # ?
    newline = (6, "newline")    # +
    string = (7, "str")         # +

    colon = (100, "colon")
    b_op = (101, "b_op")
    cb_op = (102, "cb_op")
    cb_cl = (103, "cb_cl")
    hash = (104, "hash")
    b_cl = (105, "b_cl")


class Token:
    def __init__(self, token_class: TokenClass, value: str):
        self.token_class = token_class
        self.value = value

    def __repr__(self):
        return f'Token: {self.token_class.name}'

    def __str__(self):
        return f'Token: {self.token_class.name}, value: {repr(self.value)}'

