from lexer.token import Token, TokenClass
from slr_parser.ParseTreeNode import ParseTreeNode
from syntaxer.phrase import Phrase, PhraseClass, PhraseSubclass
from syntaxer.interpretation_error import InterpretationError, PeaceError, ErrorType


ignored_list = ["Program", "Tag", "Statement", "OperatorParams", "SeparatedParam", "Param"]


def phrase_builder(context: Phrase, phrase_class: PhraseClass, node: ParseTreeNode) -> Phrase:
    if not node.name.endswith("_x") and node.name not in ignored_list:
        phrase = Phrase(phrase_class, params=list())
        if phrase_class == PhraseClass.block:
            build_block(phrase, context, node)
        elif phrase_class == PhraseClass.operator:
            build_operator(phrase, context, node)
        elif phrase_class == PhraseClass.label:
            build_label(phrase, context, node)
        else:
            raise InterpretationError(
                PeaceError(f"Unexpected phrase class.",
                           ErrorType.phrase_build_error))
        return phrase


def build_block(phrase: Phrase, context: Phrase, node: ParseTreeNode):
    phrase.keyword = node.attributes[0]

    if phrase.keyword.value == "main":
        if context.phrase_subclass == PhraseSubclass.program:
            phrase.phrase_subclass = PhraseSubclass.body
        else:
            raise InterpretationError(
                PeaceError(f"Main block can not be defined inside {context.phrase_subclass.name}.",
                           ErrorType.phrase_build_error))
    elif context.phrase_subclass == PhraseSubclass.program:
        phrase.phrase_subclass = PhraseSubclass.expression
    elif context.phrase_subclass == PhraseSubclass.body or context.phrase_subclass == PhraseSubclass.expression:
        phrase.phrase_subclass = PhraseSubclass.device
    else:
        raise InterpretationError(
            PeaceError(f"Unspecified \"{phrase.keyword.value}\" block subclass.",
                       ErrorType.phrase_build_error))

    if node.child_nodes[0].name == "Tag" and node.child_nodes[0].attributes:
        if phrase.phrase_subclass == PhraseSubclass.device:
            phrase.params = node.child_nodes[0].attributes
        else:
            raise InterpretationError(
                PeaceError(f"Not allowed to use parameters in \"{phrase.keyword.value}\" definition.",
                           ErrorType.phrase_build_error))


def build_operator(phrase: Phrase, context: Phrase, node: ParseTreeNode):
    if context.phrase_subclass != PhraseSubclass.program:
        phrase.keyword = node.attributes[0]
        # Mb here unzip parameters
        current_nodes = node.child_nodes[0].child_nodes
        while True:
            temp_nodes = list()
            if not current_nodes:
                break

            for item in current_nodes:
                if item.name == "Param":
                    if len(item.attributes) == 2:
                        phrase.params.append(Token(TokenClass.parameter, f"@{item.attributes[1].value}"))
                    else:
                        phrase.params.extend(item.attributes)
                elif item.name == "SeparatedParam":
                    if item.is_empty:
                        break
                    else:
                        temp_nodes = item.child_nodes
            else:
                if temp_nodes:
                    current_nodes = temp_nodes
                continue
            break
    else:
        raise InterpretationError(
            PeaceError(f"Operator \"{node.attributes[0].value}\" not allowed to be used outside blocks.",
                       ErrorType.phrase_build_error))


def build_label(phrase: Phrase, context: Phrase, node: ParseTreeNode):
    if context.phrase_subclass != PhraseSubclass.program:
        phrase.keyword = node.attributes[0]

        if node.child_nodes[0].name == "Tag" and node.child_nodes[0].attributes:
            if context.phrase_subclass != PhraseSubclass.expression:
                raise InterpretationError(
                    PeaceError(f"Parametrised label name can not be used inside main.",
                               ErrorType.phrase_build_error))
            else:
                phrase.params = node.child_nodes[0].attributes
    else:
        raise InterpretationError(PeaceError(f"Label \"{node.attributes[0].value}\" "
                                             f"not allowed to be used outside blocks.",
                                             ErrorType.phrase_build_error))
