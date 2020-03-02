from src.lexer.StateMachine import State
from src.lexer.lexer import Token

operators = [
    "q",
    "dq",
    "generate",
    "start",
    "delay"
]


def keyword(object):
    if object[0] == Token.word:
        if object[1] in operators:
            return State.keyword
    elif object[0] == Token.space:
        return State.begin
    return State.undefined

def firstWord(object):
    if object[0] == Token.word:
        return State.firstWord
    elif object[0] == Token.space:
        return State.begin
    return State.undefined

def parameter(object):
    if object[0] == Token.parameter:
        return State.parameter
    elif object[0] == Token.space:
        return State.parameter
    elif object[0] == Token.newline:
        return State.parameter
    return State.undefined


def undefined(object):
    return State.undefined


def equalSign(object):
    if object[0] == Token.sign:
        if object[1] == "=":
            return State.equalSign
    elif object[0] == Token.space:
        return State.firstWord
    return State.undefined


def accoladeOpenSign(object):
    if object[0] == Token.sign:
        if object[1] == "{":
            return State.accoladeOpenSign
    elif object[0] == Token.space:
        return State.equalSign
    return State.undefined
