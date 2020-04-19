from lexer.state_machine import State
from lexer.token import TokenClass, Token


def comment_start(token: Token) -> State:
    if token.token_class == TokenClass.sign:
        if token.value == "#":
            return State.comment
    elif token.token_class == TokenClass.space or token.token_class == TokenClass.newline:
        return State.begin
    return State.undefined


def comment_end(token: Token) -> State:
    if token.token_class != TokenClass.newline:
        return State.comment
    return State.undefined


def keyword(token: Token) -> State:
    if token.token_class == TokenClass.word:
        return State.openBrace
    elif token.token_class == TokenClass.space or token.token_class == TokenClass.newline:
        return State.begin
    return State.undefined


def block(token: Token) -> State:
    if token.token_class == TokenClass.word:
        return State.block_word
    elif token.token_class == TokenClass.space or token.token_class == TokenClass.newline:
        return State.begin
    return State.undefined


def block_start(token: Token) -> State:
    if token.token_class == TokenClass.sign:
        if token.value == "{":
            return State.block_end
    elif token.token_class == TokenClass.parameter:
        if token.value == "@":
            return State.block_param
    elif token.token_class == TokenClass.space or token.token_class == TokenClass.newline:
        return State.block_sign
    return State.undefined


def block_param(token: Token) -> State:
    if token.token_class == TokenClass.sign:
        if token.value == "{":
            return State.block_end
    elif token.token_class == TokenClass.space or token.token_class == TokenClass.newline:
        return State.block_param
    return State.undefined


def block_sign(token: Token) -> State:
    if token.token_class == TokenClass.sign:
        if token.value == "{":
            return State.block_end
    elif token.token_class == TokenClass.space or token.token_class == TokenClass.newline:
        return State.block_end
    return State.undefined


def block_end(token: Token) -> State:
    if token.token_class == TokenClass.space or token.token_class == TokenClass.newline:
        return State.block_end
    return State.undefined


def accolade_start(token: Token) -> State:
    if token.token_class == TokenClass.space or token.token_class == TokenClass.newline:
        return State.begin
    elif token.token_class == TokenClass.sign:
        if token.value == "}":
            return State.accoladeCloseSign
    return State.undefined


def accolade_end(token: Token) -> State:
    if token.token_class == TokenClass.space or token.token_class == TokenClass.newline:
        return State.accoladeCloseSign
    return State.undefined


def open_brace(token: Token) -> State:
    if token.token_class == TokenClass.sign:
        if token.value == "(":
            return State.parameter
    elif token.token_class == TokenClass.space:
        return State.openBrace
    return State.undefined


def parameter(token: Token) -> State:
    if (token.token_class == TokenClass.word or
            token.token_class == TokenClass.num or
            token.token_class == TokenClass.string or
            token.token_class == TokenClass.parameter):
        return State.sign
    elif token.token_class == TokenClass.space:
        return State.parameter
    elif token.token_class == TokenClass.sign:
        if token.value == ")":
            return State.operator_end
    return State.undefined


def param_sign(token: Token) -> State:
    if token.token_class == TokenClass.sign:
        if token.value == ",":
            return State.parameter
        elif token.value == ")":
            return State.operator_end
    elif token.token_class == TokenClass.space:
        return State.sign
    return State.undefined


def operator_end(token: Token) -> State:
    if token.token_class == TokenClass.space or token.token_class == TokenClass.newline:
        return State.operator_end
    return State.undefined


def undefined(token: Token) -> State:
    return State.undefined


def label(token: Token) -> State:
    if token.token_class == TokenClass.word:
        return State.label_start
    elif token.token_class == TokenClass.space or token.token_class == TokenClass.newline:
        return State.begin
    return State.undefined


def label_colon(token: Token) -> State:
    if token.token_class == TokenClass.sign:
        if token.value == ":":
            return State.label_end
    return State.undefined


def label_start(token: Token) -> State:
    if token.token_class == TokenClass.sign:
        if token.value == ":":
            return State.label_end
    elif token.token_class == TokenClass.parameter:
        if token.value == "@":
            return State.label_param
    return State.undefined
