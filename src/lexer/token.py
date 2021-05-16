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

    undefined = (0, "undefined")    # Service
    eof = (1, "eof")                # Service
    space = (2, "space")            # Service
    sign = (3, "sign")              # Service
    newline = (4, "newline")        # Service
    word = (5, "word")
    num = (6, "num")
    string = (7, "string")
    colon = (8, "colon")
    lbrace = (9, "lbrace")
    rbrace = (10, "rbrace")
    lcbrace = (11, "lcbrace")
    rcbrace = (12, "rcbrace")
    comma = (13, "comma")
    atsym = (14, "atsym")

    parameter = (100, "parameter_deprecated")
    comment = (101, "comment_deprecated")


class Token:
    def __init__(self, token_class: TokenClass, value: str):
        self.token_class = token_class
        self.value = value

    def __repr__(self):
        return f'Token: {self.token_class.name}'

    def __str__(self):
        return f'Token: {self.token_class.name}, value: {repr(self.value)}'

