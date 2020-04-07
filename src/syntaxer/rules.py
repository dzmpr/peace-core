from lexer.state_machine import State
from lexer.token import TokenClass, Token

operators = {
    "q": "QUEUE",
    "dq": "DEPART",
    "gen": "GENERATE",
    "init": "START",
    "delay": "ADVANCE",
    "destroy": "TERMINATE",
    "goto": "TRANSFER",
    "compare": "TEST",
    "var": "SAVEVALUE",
    "varinit": "INITIAL"
}


def body_start(token: Token):
    if token.token_class == TokenClass.word:
        if token.value == "main":
            return State.body
    elif token.token_class == TokenClass.space or token.token_class == TokenClass.newline:
        return State.begin
    return State.undefined


def body(token: Token):
    if token.token_class == TokenClass.sign:
        if token.value == "{":
            return State.body
    elif token.token_class == TokenClass.space or token.value == TokenClass.newline:
        return State.body
    return State.undefined


def comment_start(token: Token):
    if token.token_class == TokenClass.sign:
        if token.value == "#":
            return State.comment
    elif token.token_class == TokenClass.space or token.token_class == TokenClass.newline:
        return State.begin
    return State.undefined


def comment_end(token: Token):
    if token.token_class != TokenClass.newline:
        return State.comment
    return State.undefined


def keyword(token: Token):
    if token.token_class == TokenClass.word:
        if token.value in operators:
            return State.keyword
    elif token.token_class == TokenClass.space or token.token_class == TokenClass.newline:
        return State.begin
    return State.undefined


def device_start(token: Token):
    if token.token_class == TokenClass.word:
        if token.value != "main":
            return State.deviceStart
    elif token.token_class == TokenClass.space or token.token_class == TokenClass.newline:
        return State.begin
    return State.undefined


def device_end(token: Token):
    if token.token_class == TokenClass.sign:
        if token.value == "{":
            return State.device
    elif token.token_class == TokenClass.space or token.token_class == TokenClass.newline:
        return State.deviceStart
    return State.undefined


def accolade_start(token: Token):
    if token.token_class == TokenClass.space or token.token_class == TokenClass.newline:
        return State.begin
    elif token.token_class == TokenClass.sign:
        if token.value == "}":
            return State.accoladeCloseSign
    return State.undefined


def accolade_end(token: Token):
    if token.token_class == TokenClass.space or token.token_class == TokenClass.newline:
        return State.accoladeCloseSign
    return State.undefined


def device(token: Token):
    if token.token_class == TokenClass.space or token.token_class == TokenClass.newline:
        return State.device
    return State.undefined


def first_word(token: Token):
    if token.token_class == TokenClass.word:
        return State.firstWord
    elif token.token_class == TokenClass.space or token.token_class == TokenClass.newline:
        return State.begin
    return State.undefined


def parameter(token: Token):
    if token.token_class == TokenClass.parameter:
        return State.parameter
    elif token.token_class == TokenClass.space:
        return State.parameter
    elif token.token_class == TokenClass.newline:
        return State.parameter
    return State.undefined


def undefined(token: Token):
    return State.undefined


def equal_sign(token: Token):
    if token.token_class == TokenClass.sign:
        if token.value == "=":
            return State.equalSign
    elif token.token_class == TokenClass.space:
        return State.firstWord
    return State.undefined


def accolade_open_sign(token: Token):
    if token.token_class == TokenClass.sign:
        if token.value == "{":
            return State.accoladeOpenSign
    elif token.token_class == TokenClass.space:
        return State.equalSign
    return State.undefined


def label_start(token: Token):
    if token.token_class == TokenClass.word:
        return State.label
    elif token.token_class == TokenClass.space or token.token_class == TokenClass.newline:
        return State.begin
    return State.undefined


def label(token: Token):
    if token.token_class == TokenClass.sign:
        if token.value == ":":
            return State.label
    return State.undefined
