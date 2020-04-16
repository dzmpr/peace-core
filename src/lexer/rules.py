from lexer.state_machine import State

signList = ["+", "-", "/", "*", "=", "#", "$", "[", "]",
            "{", "}", ":", ",", "(", ")", "."]


def char(symbol):
    if symbol.isalnum():
        return State.char
    return State.undefined


def char_start(symbol):
    if symbol.isalpha():
        return State.char
    return State.undefined


def space(symbol):
    if symbol == " ":
        return State.space
    return State.undefined


def tab(symbol):
    if symbol == "\t":
        return State.tab
    return State.undefined


def num(symbol):
    if symbol.isdigit():
        return State.num
    return State.undefined


def undefined(symbol):
    return State.undefined


def sign(symbol):
    if symbol in signList:
        return State.sign
    return State.undefined


def newline(symbol):
    if symbol == "\n":
        return State.newline
    return State.undefined


def str_start(symbol):
    if symbol == "\"":
        return State.str_start
    return State.undefined


def str_body(symbol):
    if symbol.isalnum() or symbol in signList or symbol == " " or symbol == "\t":
        return State.str_start
    elif symbol == "\"":
        return State.str_end
    return State.undefined


def parameter_start(symbol):
    if symbol == "@":
        return State.parameter
    return State.undefined


def parameter(symbol):
    if symbol.isdigit():
        return State.parameter
    return State.undefined
