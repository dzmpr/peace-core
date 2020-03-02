from src.lexer.StateMachine import State

signList = ["+", "-", "/", "*", "=", "#", "$", "[", "]", "{", "}"]


def char(char):
    if char.isalnum():
        return State.char
    return State.undefined


def charStart(char):
    if char.isalpha():
        return State.char
    return State.undefined


def open(char):
    if char == "(":
        return State.openBrace
    return State.undefined


def opened(char):
    if char == " ":
        return State.openBrace
    elif char.isalnum():
        return State.openBrace
    elif char == ",":
        return State.openBrace
    elif char == ")":
        return State.closeBrace
    return State.undefined


def closed(char):
    return State.undefined


def space(char):
    if char == " ":
        return State.space
    return State.undefined


def num(char):
    if char.isdigit():
        return State.num
    return State.undefined


def undefined(char):
    return State.undefined


def sign(char):
    if char in signList:
        return State.sign
    return State.undefined


def newline(char):
    if char == "\n":
        return State.newline
    return State.undefined
