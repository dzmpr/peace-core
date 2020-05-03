from lexer.state_machine import State
from lexer.token import TokenClass, Token
from syntaxer.syntaxer_state_machine import SyntaxerStateMachine
from syntaxer.phrase import PhraseClass
from syntaxer import rules
from parsetree.parse_tree import ParseTree
from semanticanalyzer.symbol_table import SymbolTable
from semanticanalyzer.semantic_analyzer import SemanticAnalyzer
from syntaxer.interpretation_error import InterpretationError, ErrorType, PeaceError
from syntaxer.phrase_builder import phrase_builder
from syntaxer.lang_dict import LangDict
from typing import List


operatorMachine = SyntaxerStateMachine(PhraseClass.operator, State.operator_end, {
    State.begin: rules.keyword,
    State.openBrace: rules.open_brace,
    State.parameter: rules.parameter,
    State.sign: rules.param_sign,
    State.operator_end: rules.operator_end
})

commentMachine = SyntaxerStateMachine(PhraseClass.comment, State.comment, {
    State.begin: rules.comment_start,
    State.comment: rules.comment_end,
})

blockMachine = SyntaxerStateMachine(PhraseClass.block, State.block_end, {
    State.begin: rules.block,
    State.block_word: rules.block_start,
    State.block_param: rules.block_param,
    State.block_sign: rules.block_sign,
    State.block_end: rules.block_end
})

blockCloseMachine = SyntaxerStateMachine(PhraseClass.blockClose, State.accoladeCloseSign, {
    State.begin: rules.accolade_start,
    State.accoladeCloseSign: rules.accolade_end
})

labelMachine = SyntaxerStateMachine(PhraseClass.label, State.label_end, {
    State.begin: rules.label,
    State.label_start: rules.label_start,
    State.label_param: rules.label_colon,
    State.label_end: rules.undefined
})

machines = {
    operatorMachine,
    commentMachine,
    blockMachine,
    blockCloseMachine,
    labelMachine
}


def process_tokens(tree: ParseTree, table: SymbolTable, lang_dict: LangDict, tokens: List[Token]):
    active_machines: bool = False
    machine_found: bool = False
    token_index: int = 0
    phrase_start_line: int = 1
    temp_phrase: List[Token] = []
    sem_analyzer = SemanticAnalyzer(tree, table, lang_dict)

    while token_index < len(tokens):
        token: Token = tokens[token_index]

        # New line check
        if token.token_class == TokenClass.newline:
            sem_analyzer.add_line()

        # Process token
        for machine in machines:
            machine.process_object(token)
            if machine.state != State.undefined:
                active_machines = True

        # Check machine states
        if not active_machines:
            for machine in machines:
                if not machine_found and machine.is_sequence_recognized():
                    recognized_phrase = phrase_builder(tree.get_context(), machine.name, temp_phrase, phrase_start_line)
                    sem_analyzer.process_phrase(recognized_phrase, phrase_start_line)
                    machine_found = True
                    temp_phrase.clear()

            # Token wasn't recognized by any machine
            if not machine_found:
                for machine in machines:
                    if machine.prevState != State.undefined:
                        raise InterpretationError(
                            PeaceError(f"Unexpected token {repr(token.value)}.",
                                       ErrorType.syntax_error, sem_analyzer.get_line(), token.value))

            # Reset machine states
            for machine in machines:
                machine.reset_state()

            # Get new phrase start line
            phrase_start_line = sem_analyzer.get_line()

            # If current token newline - decrease line counter
            if token.token_class == TokenClass.newline:
                sem_analyzer.remove_line()

            token_index = token_index - 1
            machine_found = False
        else:
            if (token.token_class != TokenClass.space and
                    token.token_class != TokenClass.newline and
                    token.token_class != TokenClass.undefined and
                    token.token_class != TokenClass.sign):
                temp_phrase.append(token)

        token_index += 1
        active_machines = False

    for machine in machines:
        if not machine_found and machine.is_sequence_recognized():
            recognized_phrase = phrase_builder(tree.get_context(), machine.name, temp_phrase, phrase_start_line)
            sem_analyzer.process_phrase(recognized_phrase, phrase_start_line)
            machine_found = True

    if not sem_analyzer.composer.is_tree_valid():
        raise InterpretationError(
            PeaceError("Missing '}}'.", ErrorType.syntax_error, phrase_start_line))
    return
