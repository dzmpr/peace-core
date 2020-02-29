import enum
from src.lexer import state_machine
from src.lexer import rules


class states(enum.Enum):
    undefined = 0,
    begin = 1,
    char = 2,
    openBrace = 3,
    closeBrace = 4,
    openBlock = 5,
    closeBlock = 6,
    space = 7,
    num = 8,
    sign = 9


wordMachine = state_machine.StateMachine("word", {
    states.begin: rules.charStart,
    states.char: rules.char
})

paramMachine = state_machine.StateMachine("param", {
    states.begin: rules.open,
    states.openBrace: rules.opened,
    states.closeBrace: rules.closed
})

spaceMachine = state_machine.StateMachine("space", {
    states.begin: rules.space,
    states.space: rules.space
})

numberMachine = state_machine.StateMachine("num", {
    states.begin: rules.num,
    states.num: rules.num
})

signMachine = state_machine.StateMachine("sign", {
    states.begin: rules.sign,
    states.sign: rules.undefined
})

machines = {
    wordMachine,
    paramMachine,
    spaceMachine,
    numberMachine,
    signMachine
}


# lexer
def processLine(machines, str):
    tokens = []
    activeMachines = False
    index = 0
    machineFound = False
    i = 0
    while i < len(str) + 1:
        if i >= len(str):
            char = '\n'
        else:
            char = str[i]

        for machine in machines:
            machine.processObject(char)
            if machine.state != states.undefined:
                activeMachines = True

        if not activeMachines:
            for mach in machines:
                if mach.prevState != states.undefined and mach.prevState != states.begin and not machineFound:
                    tokens.append([mach.name, str[index:i]])
                    machineFound = True
                mach.resetState()
            if char == "\n":
                break
            index = i
            i = i - 1
            machineFound = False
        activeMachines = False
        i = i + 1
    return tokens
