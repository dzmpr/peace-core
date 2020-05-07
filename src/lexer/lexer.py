from lexer.state_machine import State, StateMachine
from lexer.token import Token, TokenClass
from lexer import rules
from typing import List


wordMachine = StateMachine(TokenClass.word, {
    State.begin: rules.char_start,
    State.char: rules.char
})

stringMachine = StateMachine(TokenClass.string, {
    State.begin: rules.str_start,
    State.str_start: rules.str_body,
    State.str_end: rules.undefined
})

spaceMachine = StateMachine(TokenClass.space, {
    State.begin: rules.space,
    State.space: rules.space
})
# TODO: add tab token class
tabMachine = StateMachine(TokenClass.space, {
    State.begin: rules.tab,
    State.tab: rules.tab
})

numberMachine = StateMachine(TokenClass.num, {
    State.begin: rules.num,
    State.num: rules.num
})

signMachine = StateMachine(TokenClass.sign, {
    State.begin: rules.sign,
    State.sign: rules.undefined
})

newlineMachine = StateMachine(TokenClass.newline, {
    State.begin: rules.newline,
    State.newline: rules.newline
})

parameterMachine = StateMachine(TokenClass.parameter, {
    State.begin: rules.parameter_start,
    State.parameter: rules.parameter
})

machines = {
    wordMachine,
    spaceMachine,
    tabMachine,
    numberMachine,
    signMachine,
    newlineMachine,
    stringMachine,
    parameterMachine
}


# lexer
def process_line(string: str) -> List[Token]:
    """
    Split input string in tokens.

    :param string: string to process
    :return: list contains recognized tokens
    """
    tokens: List[Token] = []
    index = 0
    i = 0
    active_machines = False
    machine_found = False

    while i < len(string):
        char = string[i]
        # Process symbol by each machine
        for machine in machines:
            machine.process_object(char)
            if machine.state != State.undefined:
                active_machines = True

        if not active_machines:
            # If all machines reach undefined state and sequence length is not zero
            if i - index > 0:
                for machine in machines:
                    # Find machine with not undefined state
                    if machine.prevState != State.undefined and machine.prevState != State.begin and not machine_found:
                        token = Token(machine.name, string[index:i])
                        tokens.append(token)
                        machine_found = True
                    machine.reset_state()
                index = i
                # Roll back for 1 symbol, that led to undefined state (and is an part of next token)
                i -= 1
                machine_found = False
            # If all machines reach undefined state and current symbol was not recognized
            else:
                # Classify symbol as undefined
                tokens.append(Token(TokenClass.undefined, string[i]))
                index = i
        # Reset active machines flag
        active_machines = False
        i += 1

    # Recognize final token
    for machine in machines:
        if machine.state != State.undefined and machine.state != State.begin and not machine_found:
            token = Token(machine.name, string[index:i])
            tokens.append(token)
            machine_found = True
        machine.reset_state()

    return tokens
