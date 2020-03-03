from src.lexer.StateMachine import State
from src.lexer.lexer import Token

operators = {
    "q": "QUEUE",
    "dq": "DEPART",
    "gen": "GENERATE",
    "init": "START",
    "delay": "ADVANCE",
    "destroy": "TERMINATE",
    "goto": "TRANSFER"
}


def bodyStart(object):
    if object[0] == Token.word:
        if object[1] == "main":
            return State.body
    elif object[0] == Token.space or object[0] == Token.newline:
        return State.begin
    return State.undefined


def body(object):
    if object[0] == Token.sign:
        if object[1] == "{":
            return State.body
    elif object[0] == Token.space or object[0] == Token.newline:
        return State.body
    return State.undefined


def commentStart(object):
    if object[0] == Token.sign:
        if object[1] == "#":
            return State.comment
    elif object[0] == Token.space or object[0] == Token.newline:
        return State.begin
    return State.undefined


def commentEnd(object):
    if object[0] != Token.newline:
        return State.comment
    return State.undefined


def keyword(object):
    if object[0] == Token.word:
        if object[1] in operators:
            return State.keyword
    elif object[0] == Token.space or object[0] == Token.newline:
        return State.begin
    return State.undefined


def deviceStart(object):
    if object[0] == Token.word:
        if object[1] != "main":
            return State.deviceStart
    elif object[0] == Token.space or object[0] == Token.newline:
        return State.begin
    return State.undefined


def deviceEnd(object):
    if object[0] == Token.sign:
        if object[1] == "{":
            return State.device
    elif object[0] == Token.space or object[0] == Token.newline:
        return State.deviceStart
    return State.undefined


def accoladeStart(object):
    if object[0] == Token.sign:
        if object[1] == "}":
            return State.accoladeCloseSign
    return State.undefined

def accoladeEnd(object):
    if object[0] == Token.space or object[0] == Token.newline:
        return State.accoladeCloseSign
    return State.undefined

def device(object):
    if object[0] == Token.space or object[0] == Token.newline:
        return State.device
    return State.undefined


def firstWord(object):
    if object[0] == Token.word:
        return State.firstWord
    elif object[0] == Token.space or object[0] == Token.newline:
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
