from lexer.state_machine import State

signList = ["+", "-", "/", "*", "=", "#", "$", "[", "]", "{", "}", ":", ",", "(", ")", "."]


def char(char):
    if char.isalnum():
        return State.char
    return State.undefined


def char_start(char):
    if char.isalpha():
        return State.char
    return State.undefined


def space(char):
    if char == " ":
        return State.space
    return State.undefined


def tab(char):
    if char == "\t":
        return State.tab
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


def str_start(char):
    if char == "\"":
        return State.str_start
    return State.undefined


def str_body(char):
    if char.isalnum() or char in signList or char == " " or char == "\t":
        return State.str_start
    elif char == "\"":
        return State.str_end
    return State.undefined
