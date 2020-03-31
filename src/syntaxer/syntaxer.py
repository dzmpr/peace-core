from src.lexer.StateMachine import State
from src.lexer.Token import TokenClass, Token
from src.syntaxer.SyntaxerStateMachine import SyntaxerStateMachine
from src.syntaxer.Phrase import PhraseClass
from src.syntaxer.SemanticProcessor import SemanticProcessor, SyntaxParseError
from src.syntaxer import rules

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


def process_tokens(tokens):
    output = []
    active_machines = False
    machine_found = False
    i = 0
    temp_phrase = []
    semantic_processor = SemanticProcessor()
    while i < len(tokens):
        token: Token = tokens[i]

        # New line check
        if token.name == TokenClass.newline:
            semantic_processor.next_line()

        # Process token
        for machine in machines:
            machine.process_object(token)
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
                    semantic_processor.process_phrase(phrase)

            if token.name == TokenClass.undefined:
                if not semantic_processor.is_block_closed():
                    raise SyntaxParseError("Syntax error. Bad scoping.")
                return output

            # Token wasn't recognized by any machine
            if not machine_found:
                for machine in machines:
                    if machine.prevState != State.undefined:
                        raise SyntaxParseError("Syntax error. Expected {} at line {}.".format(machine.name, semantic_processor.processed_lines()))

            # Reset machine states
            for machine in machines:
                machine.reset_state()

            i = i - 1
            machine_found = False
        else:
            if token.name != TokenClass.space and \
                    token.name != TokenClass.newline and \
                    token.name != TokenClass.undefined and \
                    token.name != TokenClass.sign:
                temp_phrase.append(token)

        i = i + 1
        active_machines = False

    return output
