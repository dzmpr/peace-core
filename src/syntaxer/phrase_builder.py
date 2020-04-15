from syntaxer.phrase import Phrase, PhraseClass, PhraseSubclass
from lexer.token import Token, TokenClass
from typing import List


class PhraseBuildError(Exception):
    def __init__(self, msg):
        self.msg = msg


def phrase_builder(context: PhraseSubclass, phrase_class: PhraseClass, temp_phrase: List[Token]) -> Phrase:
    phrase = Phrase(phrase_class)
    if phrase_class == PhraseClass.block:
        build_block(phrase, context, temp_phrase)
    elif phrase_class == PhraseClass.operator:
        build_operator(phrase, context, temp_phrase)
    elif phrase_class == PhraseClass.comment:
        build_comment(phrase, temp_phrase)
    elif phrase_class == PhraseClass.label:
        build_label(phrase, context, temp_phrase)
    elif phrase_class == PhraseClass.blockClose:
        build_block_close(phrase, temp_phrase)
    else:
        raise PhraseBuildError("Unexpected phrase class.")
    return phrase


def build_block(phrase: Phrase, context: PhraseSubclass, temp_phrase: List[Token]):
    if temp_phrase[0].token_class == TokenClass.word:
        phrase.keyword = temp_phrase[0]
    else:
        raise PhraseBuildError("Unexpected phrase sequence.")

    if phrase.keyword.value == "main":
        if context == PhraseSubclass.program:
            phrase.phrase_subclass = PhraseSubclass.body
        else:
            # TODO: work out
            raise PhraseBuildError("Incorrect naming.")
    elif context == PhraseSubclass.program:
        phrase.phrase_subclass = PhraseSubclass.expression
    elif context == PhraseSubclass.body or context == PhraseSubclass.expression:
        phrase.phrase_subclass = PhraseSubclass.device


def build_operator(phrase: Phrase, context: PhraseSubclass, temp_phrase: List[Token]):
    if context != PhraseSubclass.program:
        if temp_phrase[0].token_class == TokenClass.word:
            phrase.keyword = temp_phrase[0]
        else:
            raise PhraseBuildError("Unexpected phrase sequence.")

        phrase.params = temp_phrase[1:]
    else:
        raise PhraseBuildError(f"Operator \"{temp_phrase[0].value}\" not allowed to be used outside blocks.")


def build_comment(phrase: Phrase, temp_phrase: List[Token]):
    phrase.params = temp_phrase


def build_label(phrase: Phrase, context: PhraseSubclass, temp_phrase: List[Token]):
    if context != PhraseSubclass.program:
        if temp_phrase[0].token_class == TokenClass.word:
            phrase.keyword = temp_phrase[0]
        else:
            raise PhraseBuildError("Unexpected phrase sequence.")
    else:
        raise PhraseBuildError(f"Label \"{temp_phrase[0].value}\" not allowed to be used outside blocks.")


def build_block_close(phrase: Phrase, temp_phrase: List[Token]):
    pass
