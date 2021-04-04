from enum import Enum


class TokenType(Enum):
    TOKEN_STR = (0, "a")
    TOKEN_NUM = (1, "b")
    TOKEN_SIGN = (2, "c")
    TOKEN_EOF = (9999, "d")

    def __init__(self, t_id, t_name):
        self.t_id = t_id
        self.t_name = t_name


class Token:
    def __init__(self, token_type: TokenType, token_value: str):
        self.token_type: TokenType = token_type
        self.token_value: str = token_value

    def __repr__(self):
        return f"{self.token_type.name}: {self.token_value}"
