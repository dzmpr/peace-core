from lexer.StateMachine import State
from lexer.Token import TokenClass, Token
from syntaxer.SyntaxerStateMachine import SyntaxerStateMachine
from syntaxer.Phrase import PhraseClass, Phrase
from syntaxer import rules
from parsetree.ParseTree import ParseTree
from parsetree.TreeComposer import TreeComposer
from SemanticAnalyzer.SymbolTable import SymbolTable
from SemanticAnalyzer.SemanticAnalyzer import SemanticAnalyzer
from typing import List


class SyntaxParseError(Exception):
    def __init__(self, msg):
        self.msg = msg


operatorMachine = SyntaxerStateMachine(PhraseClass.operator, State.parameter, {
    State.begin: rules.keyword,
    State.keyword: rules.parameter,
    State.parameter: rules.parameter
})

expressionMachine = SyntaxerStateMachine(PhraseClass.expression, State.accoladeOpenSign, {
    State.begin: rules.first_word,
    State.firstWord: rules.equal_sign,
    State.equalSign: rules.accolade_open_sign,
    State.accoladeOpenSign: rules.accolade_open_sign
})

commentMachine = SyntaxerStateMachine(PhraseClass.comment, State.comment, {
    State.begin: rules.comment_start,
    State.comment: rules.comment_end,
})

bodyMachine = SyntaxerStateMachine(PhraseClass.body, State.body, {
    State.begin: rules.body_start,
    State.body: rules.body
})

deviceMachine = SyntaxerStateMachine(PhraseClass.device, State.device, {
    State.begin: rules.device_start,
    State.deviceStart: rules.device_end,
    State.device: rules.device
})

blockCloseMachine = SyntaxerStateMachine(PhraseClass.blockClose, State.accoladeCloseSign, {
    State.begin: rules.accolade_start,
    State.accoladeCloseSign: rules.accolade_end
})

labelMachine = SyntaxerStateMachine(PhraseClass.label, State.label, {
    State.begin: rules.label_start,
    State.label: rules.label
})

machines = {
    operatorMachine,
    expressionMachine,
    commentMachine,
    bodyMachine,
    deviceMachine,
    blockCloseMachine,
    labelMachine
}


def process_tokens(tree: ParseTree, table: SymbolTable, tokens: List[Token]):
    active_machines: bool = False
    machine_found: bool = False
    token_index: int = 0
    line_counter: int = 0
    temp_phrase: List[Token] = []
    tree_composer = TreeComposer(tree)
    sem_analyzer = SemanticAnalyzer(tree, table)

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
                    recognized_phrase = Phrase(machine.name, temp_phrase.copy())
                    sem_analyzer.process_phrase(recognized_phrase)
                    tree_composer.add_phrase(recognized_phrase)
                    machine_found = True
                    temp_phrase.clear()

            if token.token_class == TokenClass.undefined:
                if not tree_composer.is_tree_valid():
                    raise SyntaxParseError("Syntax error. Bad scoping.")
                return

            # Token wasn't recognized by any machine
            if not machine_found:
                for machine in machines:
                    if machine.prevState != State.undefined:
                        raise SyntaxParseError(f"Syntax error. Expected {machine.name.name} at line {line_counter}.")

            # Reset machine states
            for machine in machines:
                machine.reset_state()

            token_index = token_index - 1
            machine_found = False
        else:
            if token.token_class != TokenClass.space and \
                    token.token_class != TokenClass.newline and \
                    token.token_class != TokenClass.undefined and \
                    token.token_class != TokenClass.sign:
                temp_phrase.append(token)

        token_index += 1
        active_machines = False

    return
