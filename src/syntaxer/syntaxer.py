from lexer.state_machine import State
from lexer.token import TokenClass, Token
from syntaxer.syntaxer_state_machine import SyntaxerStateMachine
from syntaxer.phrase import PhraseClass
from syntaxer import rules
from parsetree.parse_tree import ParseTree
from parsetree.tree_composer import TreeComposer
from semanticanalyzer.symbol_table import SymbolTable
from semanticanalyzer.semantic_analyzer import SemanticAnalyzer
from syntaxer.phrase_builder import phrase_builder
from syntaxer.lang_dict import LangDict
from typing import List


class SyntaxParseError(Exception):
    def __init__(self, msg):
        self.msg = msg


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

blockMachine = SyntaxerStateMachine(PhraseClass.block, State.block, {
    State.begin: rules.block_start,
    State.blockStart: rules.block_end,
    State.block: rules.block
})

blockCloseMachine = SyntaxerStateMachine(PhraseClass.blockClose, State.accoladeCloseSign, {
    State.begin: rules.accolade_start,
    State.accoladeCloseSign: rules.accolade_end
})

labelMachine = SyntaxerStateMachine(PhraseClass.label, State.label_end, {
    State.begin: rules.label,
    State.label: rules.label_start,
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
    line_counter: int = 0
    temp_phrase: List[Token] = []
    tree_composer = TreeComposer(tree)
    sem_analyzer = SemanticAnalyzer(tree, table, lang_dict)

    while token_index < len(tokens):
        token: Token = tokens[token_index]

        # New line check
        if token.token_class == TokenClass.newline:
            line_counter += 1

        # Process token
        for machine in machines:
            machine.process_object(token)
            if machine.state != State.undefined:
                active_machines = True

        # Check machine states
        if not active_machines:
            for machine in machines:
                if not machine_found and machine.is_sequence_recognized():
                    recognized_phrase = phrase_builder(tree.get_context(), machine.name, temp_phrase)
                    sem_analyzer.process_phrase(recognized_phrase)
                    tree_composer.add_phrase(recognized_phrase)
                    machine_found = True
                    temp_phrase.clear()

            # Token wasn't recognized by any machine
            if not machine_found:
                for machine in machines:
                    if machine.prevState != State.undefined:
                        raise SyntaxParseError(f"Syntax error. Unexpected token "
                                               f"{repr(token.value)} at line {line_counter}.")

            # Reset machine states
            for machine in machines:
                machine.reset_state()

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
            recognized_phrase = phrase_builder(tree.get_context(), machine.name, temp_phrase)
            sem_analyzer.process_phrase(recognized_phrase)
            tree_composer.add_phrase(recognized_phrase)
            machine_found = True

    if not tree_composer.is_tree_valid():
        raise SyntaxParseError("Syntax error. Bad scoping.")
    return
