from enum import Enum


class TokenClass(Enum):
    def __repr__(self):
        return self.name

    word = 0
    parameter = 1
    space = 2
    num = 3
    sign = 4
    newline = 5
    undefined = 6


class Token:
    def __init__(self, token_class: TokenClass, value: str):
        self.token_class = token_class
        self.value = value

    def __repr__(self):
        return f'Token: {self.token_class.name}'

    def __str__(self):
        return f'Token: {self.token_class.name}, value: {repr(self.value)}'

