from syntaxer.phrase import Phrase, PhraseClass, PhraseSubclass
from lexer.token import Token, TokenClass
from syntaxer.interpretation_error import InterpretationError, PeaceError, ErrorType
from typing import List


def phrase_builder(context: Phrase, phrase_class: PhraseClass, temp_phrase: List[Token], phrase_line: int) -> Phrase:
    phrase = Phrase(phrase_class, params=list())
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
        raise InterpretationError(
            PeaceError(f"Unexpected phrase class.",
                       ErrorType.phrase_build_error, phrase_line))
    return phrase


def build_block(phrase: Phrase, context: Phrase, temp_phrase: List[Token], phrase_line: int):
    if temp_phrase[0].token_class == TokenClass.word:
        phrase.keyword = temp_phrase[0]
    else:
        raise InterpretationError(
            PeaceError(f"Unexpected phrase sequence.",
                       ErrorType.phrase_build_error, phrase_line))

    if phrase.keyword.value == "main":
        if context.phrase_subclass == PhraseSubclass.program:
            phrase.phrase_subclass = PhraseSubclass.body
        else:
            raise InterpretationError(
                PeaceError(f"Main block can not be defined inside {context.phrase_subclass.name}.",
                           ErrorType.phrase_build_error, phrase_line))
    elif context.phrase_subclass == PhraseSubclass.program:
        phrase.phrase_subclass = PhraseSubclass.expression
    elif context.phrase_subclass == PhraseSubclass.body or context.phrase_subclass == PhraseSubclass.expression:
        phrase.phrase_subclass = PhraseSubclass.device
    else:
        raise InterpretationError(
            PeaceError(f"Unspecified \"{phrase.keyword.value}\" block subclass.",
                       ErrorType.phrase_build_error, phrase_line))

    if len(temp_phrase) > 1:
        if phrase.phrase_subclass == PhraseSubclass.device:
            phrase.params = temp_phrase[1:]
        else:
            raise InterpretationError(
                PeaceError(f"Not allowed to use parameters in \"{phrase.keyword.value}\" definition.",
                           ErrorType.phrase_build_error, phrase_line))


def build_operator(phrase: Phrase, context: Phrase, temp_phrase: List[Token], phrase_line):
    if context.phrase_subclass != PhraseSubclass.program:
        if temp_phrase[0].token_class == TokenClass.word:
            phrase.keyword = temp_phrase[0]
        else:
            raise InterpretationError(
                PeaceError(f"Unexpected phrase sequence.",
                           ErrorType.phrase_build_error, phrase_line))

        phrase.params = temp_phrase[1:]
    else:
        raise InterpretationError(
            PeaceError(f"Operator \"{temp_phrase[0].value}\" not allowed to be used outside blocks.",
                       ErrorType.phrase_build_error, phrase_line))


def build_comment(phrase: Phrase, temp_phrase: List[Token]):
    phrase.params = temp_phrase


def build_label(phrase: Phrase, context: Phrase, temp_phrase: List[Token], phrase_line):
    if context.phrase_subclass != PhraseSubclass.program:
        if temp_phrase[0].token_class == TokenClass.word:
            phrase.keyword = temp_phrase[0]
        else:
            raise InterpretationError(
                PeaceError(f"Unexpected phrase sequence.",
                           ErrorType.phrase_build_error, phrase_line))

        if len(temp_phrase) > 1 and context.phrase_subclass != PhraseSubclass.expression:
            raise InterpretationError(
                PeaceError(f"Parametrised label name can not be used inside main.",
                           ErrorType.phrase_build_error, phrase_line))
        else:
            phrase.params = temp_phrase[1:]
    else:
        raise InterpretationError(PeaceError(f"Label \"{temp_phrase[0].value}\" "
                                             f"not allowed to be used outside blocks.",
                                             ErrorType.phrase_build_error, phrase_line))


def build_block_close(phrase: Phrase, temp_phrase: List[Token]):
    pass
