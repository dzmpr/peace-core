from enum import Enum


class TokenClass(Enum):
    def __repr__(self):
        return self.name

    undefined = 0
    word = 1
    parameter = 2
    space = 3
    num = 4
    sign = 5
    newline = 6
    string = 7


class Token:
    def __init__(self, token_class: TokenClass, value: str):
        self.token_class = token_class
        self.value = value

    def __repr__(self):
        return f'Token: {self.token_class.name}'

    def __str__(self):
        return f'Token: {self.token_class.name}, value: {repr(self.value)}'

