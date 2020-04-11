from lexer.state_machine import State, StateMachine
from lexer.token import Token, TokenClass
from lexer import rules
from typing import List


wordMachine = StateMachine(TokenClass.word, {
    State.begin: rules.char_start,
    State.char: rules.char
})

paramMachine = StateMachine(TokenClass.parameter, {
    State.begin: rules.open,
    State.openBrace: rules.opened,
    State.closeBrace: rules.closed
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

machines = {
    wordMachine,
    paramMachine,
    spaceMachine,
    tabMachine,
    numberMachine,
    signMachine,
    newlineMachine,
    stringMachine
}


# lexer
def process_line(string: str) -> List[Token]:
    tokens: List[Token] = []
    index = 0
    i = 0
    active_machines = False
    machine_found = False
    while i < len(string):
        char = string[i]
        for machine in machines:
            machine.process_object(char)
            if machine.state != State.undefined:
                active_machines = True

        if not active_machines:
            for machine in machines:
                if machine.prevState != State.undefined and machine.prevState != State.begin and not machine_found:
                    token = Token(machine.name, string[index:i])
                    tokens.append(token)
                    machine_found = True
                machine.reset_state()
            index = i
            i = i - 1
            machine_found = False
        active_machines = False
        i = i + 1

    for machine in machines:
        if machine.state == State.newline:
            tokens.append(Token(machine.name, string[-1:]))
        machine.reset_state()
    return tokens
