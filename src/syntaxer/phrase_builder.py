from syntaxer.phrase import Phrase, PhraseClass, PhraseSubclass
from lexer.token import Token, TokenClass
from typing import List, Union


class PhraseBuildError(Exception):
    def __init__(self,
                 msg: str,
                 line: Union[int, None] = None):
        self.msg = msg
        self.line = line


def phrase_builder(context: Phrase, phrase_class: PhraseClass, temp_phrase: List[Token], phrase_line: int) -> Phrase:
    phrase = Phrase(phrase_class)
    if phrase_class == PhraseClass.block:
        build_block(phrase, context, temp_phrase, phrase_line)
    elif phrase_class == PhraseClass.operator:
        build_operator(phrase, context, temp_phrase, phrase_line)
    elif phrase_class == PhraseClass.comment:
        build_comment(phrase, temp_phrase)
    elif phrase_class == PhraseClass.label:
        build_label(phrase, context, temp_phrase, phrase_line)
    elif phrase_class == PhraseClass.blockClose:
        build_block_close(phrase, temp_phrase)
    else:
        raise PhraseBuildError(f"Phrase build error at line {phrase_line}.\n"
                               f"Unexpected phrase class.", phrase_line)
    return phrase


def build_block(phrase: Phrase, context: Phrase, temp_phrase: List[Token], phrase_line: int):
    if temp_phrase[0].token_class == TokenClass.word:
        phrase.keyword = temp_phrase[0]
    else:
        raise PhraseBuildError(f"Phrase build error at line {phrase_line}.\n"
                               f"Unexpected phrase sequence.", phrase_line)

    if phrase.keyword.value == "main":
        if context.phrase_subclass == PhraseSubclass.program:
            phrase.phrase_subclass = PhraseSubclass.body
        else:
            raise PhraseBuildError(f"Phrase build error at line {phrase_line}.\n"
                                   f"Main block can not be defined inside {context.phrase_subclass.name}.", phrase_line)
    elif context.phrase_subclass == PhraseSubclass.program:
        phrase.phrase_subclass = PhraseSubclass.expression
    elif context.phrase_subclass == PhraseSubclass.body or context.phrase_subclass == PhraseSubclass.expression:
        phrase.phrase_subclass = PhraseSubclass.device
    else:
        raise PhraseBuildError(f"Phrase build error at line {phrase_line}.\n"
                               f"Unspecified \"{phrase.keyword.value}\" block subclass.",
                               phrase_line)


def build_operator(phrase: Phrase, context: Phrase, temp_phrase: List[Token], phrase_line):
    if context.phrase_subclass != PhraseSubclass.program:
        if temp_phrase[0].token_class == TokenClass.word:
            phrase.keyword = temp_phrase[0]
        else:
            raise PhraseBuildError(f"Phrase build error at line {phrase_line}.\n"
                                   f"Unexpected phrase sequence.", phrase_line)

        phrase.params = temp_phrase[1:]
    else:
        raise PhraseBuildError(f"Phrase build error at line {phrase_line}.\n"
                               f"Operator \"{temp_phrase[0].value}\" not allowed to be used outside blocks.",
                               phrase_line)


def build_comment(phrase: Phrase, temp_phrase: List[Token]):
    phrase.params = temp_phrase


def build_label(phrase: Phrase, context: Phrase, temp_phrase: List[Token], phrase_line):
    if context.phrase_subclass != PhraseSubclass.program:
        if temp_phrase[0].token_class == TokenClass.word:
            phrase.keyword = temp_phrase[0]
        else:
            raise PhraseBuildError(f"Phrase build error at line {phrase_line}.\n"
                                   f"Unexpected phrase sequence.", phrase_line)
    else:
        raise PhraseBuildError(f"Phrase build error at line {phrase_line}.\n"
                               f"Label \"{temp_phrase[0].value}\" not allowed to be used outside blocks.", phrase_line)


def build_block_close(phrase: Phrase, temp_phrase: List[Token]):
    pass
