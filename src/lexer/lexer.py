from enum import Enum
from src.lexer.StateMachine import State
from src.lexer.StateMachine import StateMachine
from src.lexer import rules


class Token(Enum):
    def __repr__(self):
        return self.name

    word = 0
    parameter = 1
    space = 2
    num = 3
    sign = 4
    newline = 5
    undefined = 6


wordMachine = StateMachine(Token.word, {
    State.begin: rules.charStart,
    State.char: rules.char
})

paramMachine = StateMachine(Token.parameter, {
    State.begin: rules.open,
    State.openBrace: rules.opened,
    State.closeBrace: rules.closed
})

spaceMachine = StateMachine(Token.space, {
    State.begin: rules.space,
    State.space: rules.space
})

numberMachine = StateMachine(Token.num, {
    State.begin: rules.num,
    State.num: rules.num
})

signMachine = StateMachine(Token.sign, {
    State.begin: rules.sign,
    State.sign: rules.undefined
})

newlineMachine = StateMachine(Token.newline, {
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
def processLine(machines, str):
    tokens = []
    index = 0
    i = 0
    activeMachines = False
    machineFound = False
    while i < len(str):
        char = str[i]
        for machine in machines:
            machine.processObject(char)
            if machine.state != State.undefined:
                activeMachines = True

        if not activeMachines:
            for machine in machines:
                if machine.prevState != State.undefined and machine.prevState != State.begin and not machineFound:
                    tokens.append([machine.name, str[index:i]])
                    machineFound = True
                machine.resetState()
            index = i
            i = i - 1
            machineFound = False
        activeMachines = False
        i = i + 1

    for machine in machines:
        if machine.state == State.newline:
            tokens.append([machine.name, str[-1:]])
        machine.resetState()
    return tokens
