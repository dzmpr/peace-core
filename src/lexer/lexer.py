from src.lexer.StateMachine import State, StateMachine
from src.lexer.Token import Token, TokenGroup
from src.lexer import rules


wordMachine = StateMachine(TokenGroup.word, {
    State.begin: rules.charStart,
    State.char: rules.char
})

paramMachine = StateMachine(TokenGroup.parameter, {
    State.begin: rules.open,
    State.openBrace: rules.opened,
    State.closeBrace: rules.closed
})

spaceMachine = StateMachine(TokenGroup.space, {
    State.begin: rules.space,
    State.space: rules.space
})

numberMachine = StateMachine(TokenGroup.num, {
    State.begin: rules.num,
    State.num: rules.num
})

signMachine = StateMachine(TokenGroup.sign, {
    State.begin: rules.sign,
    State.sign: rules.undefined
})

newlineMachine = StateMachine(TokenGroup.newline, {
    State.begin: rules.newline,
    State.newline: rules.newline
})

machines = {
    wordMachine,
    paramMachine,
    spaceMachine,
    numberMachine,
    signMachine,
    newlineMachine
}


# lexer
def process_line(machines, string):
    tokens = []
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
