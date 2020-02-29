from src.lexer import lexer

signList = ["+","-","/","*","=","#","$","[","]","{","}"]


def char(char):
    if char.isalnum():
        return lexer.states.char
    return lexer.states.undefined


def charStart(char):
    if char.isalpha():
        return lexer.states.char
    return lexer.states.undefined


def open(char):
    if char == "(":
        return lexer.states.openBrace
    return lexer.states.undefined


def opened(char):
    if char == " ":
        return lexer.states.openBrace
    elif char.isalnum():
        return lexer.states.openBrace
    elif char == ",":
        return lexer.states.openBrace
    elif char == ")":
        return lexer.states.closeBrace
    return lexer.states.undefined


def closed(char):
    return lexer.states.undefined


def block(char):
    if char == "{":
        return lexer.states.openBlock
    elif char.isalpha() or char.isdigit():
        return lexer.states.openBlock
    elif char == "}":
        return lexer.states.closeBlock
    return lexer.states.undefined


def space(char):
    if char == " ":
        return lexer.states.space
    return lexer.states.undefined


def num(char):
    if char.isdigit():
        return lexer.states.num
    return lexer.states.undefined


def undefined(char):
    return lexer.states.undefined


def sign(char):
    if char in signList:
        return lexer.states.sign
    return lexer.states.undefined
