from enum import Enum


class TokenGroup(Enum):
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
    def __init__(self, name: TokenGroup, value: str):
        self.name = name
        self.value = value

    def __repr__(self):
        return f'Token: {self.name.name}'

    def __str__(self):
        return f'Token: {self.name.name}, value: {repr(self.value)}'

