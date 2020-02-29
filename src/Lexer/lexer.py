import enum


class states(enum.Enum):
    undefined = 0,
    begin = 1,
    char = 2,
    openBrace = 3,
    closeBrace = 4,
    openBlock = 5,
    closeBlock = 6


def char(char):
    if char.isalnum():
        return states.char
    return states.undefined


def open(char):
    if char == "(":
        return states.openBrace
    return states.undefined


def opened(char):
    if char == " ":
        return states.openBrace
    elif char.isalnum():
        return states.openBrace
    elif char == ")":
        return states.closeBrace
    return states.undefined


def closed(char):
    return states.undefined


def block(char):
    if char == "{":
        return states.openBlock
    elif char.isalpha() or char.isdigit():
        return states.openBlock
    elif char == "}":
        return states.closeBlock
    return states.undefined


class StateMachine:
    def __init__(self, name, rules):
        self.state = states.begin
        self.prevState = states.begin
        self.rules = rules
        self.name = name

    def __str__(self):
        return self.name

    def processChar(self, char):
        self.prevState = self.state
        if self.state != states.undefined:
            self.state = self.rules[self.prevState](char)

    def resetState(self):
        self.prevState = states.begin
        self.state = states.begin
