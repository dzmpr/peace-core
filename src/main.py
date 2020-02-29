import sys
from src.Lexer import lexer

# # Checking if file path was provided
# if len(sys.argv) < 2:
#     print("Too less arguments.")
#     exit()
# # Checking if file has correct extension
# if sys.argv[1][-4:] != "pyss":
#     print("Incorrect file.")
#     exit()

# print("Input file: {}".format(sys.argv[1]))

# Lexer
wordMachine = lexer.StateMachine("word", {
    lexer.states.begin: lexer.char,
    lexer.states.char: lexer.char
})

paramMachine = lexer.StateMachine("param", {
    lexer.states.begin: lexer.open,
    lexer.states.openBrace: lexer.opened,
    lexer.states.closeBrace: lexer.closed
})

str = input("String to parse: ")
machines = {
    wordMachine,
    paramMachine
}
tokens = []
activeMachines = False
index = 0
machineFound = False
for i in range(len(str)+1):
    if i >= len(str):
        char = '\0'
    else:
        char = str[i]

    for machine in machines:
        machine.processChar(char)
        if machine.state != lexer.states.undefined:
            activeMachines = True

    if not activeMachines:
        for mach in machines:
            if mach.prevState != lexer.states.undefined and not machineFound:
                tokens.append([mach.name, str[index:i]])
                machineFound = True
            mach.resetState()
        index = i
        i = i - 1
        machineFound = False
    activeMachines = False

print(tokens)

