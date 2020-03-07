from src.lexer.StateMachine import State
from src.lexer.Token import TokenGroup, Token
from src.syntaxer.SyntaxerStateMachine import SyntaxerStateMachine
from src.syntaxer.SyntaxerStateMachine import PhraseGroup
from src.syntaxer.SemanticProcessor import SemanticProcessor
from src.syntaxer.SemanticProcessor import SyntaxParseError
from src.syntaxer import rules

operatorMachine = SyntaxerStateMachine(PhraseGroup.operator, State.parameter, {
    State.begin: rules.keyword,
    State.keyword: rules.parameter,
    State.parameter: rules.parameter
})

expressionMachine = SyntaxerStateMachine(PhraseGroup.expression, State.accoladeOpenSign, {
    State.begin: rules.first_word,
    State.firstWord: rules.equal_sign,
    State.equalSign: rules.accolade_open_sign,
    State.accoladeOpenSign: rules.accolade_open_sign
})

commentMachine = SyntaxerStateMachine(PhraseGroup.comment, State.comment, {
    State.begin: rules.comment_start,
    State.comment: rules.comment_end,
})

bodyMachine = SyntaxerStateMachine(PhraseGroup.body, State.body, {
    State.begin: rules.body_start,
    State.body: rules.body
})

deviceMachine = SyntaxerStateMachine(PhraseGroup.device, State.device, {
    State.begin: rules.device_start,
    State.deviceStart: rules.device_end,
    State.device: rules.device
})

blockCloseMachine = SyntaxerStateMachine(PhraseGroup.blockClose, State.accoladeCloseSign, {
    State.begin: rules.accolade_start,
    State.accoladeCloseSign: rules.accolade_end
})

machines = {
    operatorMachine,
    expressionMachine,
    commentMachine,
    bodyMachine,
    deviceMachine,
    blockCloseMachine
}


def process_tokens(machines, tokens):
    output = []
    active_machines = False
    machine_found = False
    i = 0
    temp_phrase = []
    phrase = []
    checker = SemanticProcessor()
    while i < len(tokens):
        token: Token = tokens[i]

        # New line check
        if token.name == TokenGroup.newline:
            checker.next_line()

        # Process token
        for machine in machines:
            machine.processObject(token)
            if machine.state != State.undefined:
                active_machines = True

        # Check machine states
        if not active_machines:
            for machine in machines:
                if not machine_found and machine.is_sequence_recognized():
                    phrase = [machine.name, temp_phrase.copy()]
                    output.append(phrase)
                    machine_found = True
                    temp_phrase.clear()
                    checker.process_phrase(phrase)

            if token.name == TokenGroup.undefined:
                if not checker.is_block_closed():
                    raise SyntaxParseError("Syntax error. Bad scoping.")
                return output

            # Token wasn't recognized by any machine
            if not machine_found:
                for machine in machines:
                    if machine.prevState != State.undefined:
                        raise SyntaxParseError("Syntax error. Expected {} at line {}.".format(machine.name, checker.processed_lines()))

            # Reset machine states
            for machine in machines:
                machine.resetState()

            i = i - 1
            machine_found = False
        else:
            if token.name != TokenGroup.space and \
                    token.name != TokenGroup.newline and \
                    token.name != TokenGroup.undefined and \
                    token.name != TokenGroup.sign:
                temp_phrase.append(token)

        i = i + 1
        active_machines = False

    return output
