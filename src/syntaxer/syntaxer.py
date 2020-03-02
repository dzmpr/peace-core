from src.lexer.StateMachine import State
from src.lexer.lexer import Token
from src.syntaxer.SyntaxerStateMachine import SyntaxerStateMachine
from src.syntaxer.SyntaxerStateMachine import Phrase
from src.syntaxer import rules


class SyntaxerError(Exception):
    def __init__(self, expectedToken, foundToken):
        self.expectedToken = expectedToken
        self.foundToken = foundToken


operatorMachine = SyntaxerStateMachine(Phrase.operator, State.parameter, {
    State.begin: rules.keyword,
    State.keyword: rules.parameter,
    State.parameter: rules.parameter
})

expressionMachine = SyntaxerStateMachine(Phrase.expression, State.accoladeOpenSign, {
    State.begin: rules.firstWord,
    State.firstWord: rules.equalSign,
    State.equalSign: rules.accoladeOpenSign,
    State.accoladeOpenSign: rules.accoladeOpenSign
})

machines = {
    operatorMachine,
    expressionMachine
}


def processTokens(machines, tokens):
    output = []
    activeMachines = False
    machineFound = False
    i = 0
    tempPhrase = dict()
    while i < len(tokens):
        token = tokens[i]
        for machine in machines:
            machine.processObject(token)
            if machine.state != State.undefined:
                activeMachines = True

        if not activeMachines:
            for machine in machines:
                if not machineFound and machine.sequenceRecognized():
                    output.append([machine.name, tempPhrase.copy()])
                    tempPhrase.clear()
                machine.resetState()
            if not machineFound:
                raise SyntaxerError("1","2")
            i = i - 1
            machineFound = False
        else:
            if token[0] != Token.space and \
                    token[0] != Token.newline and \
                    token[0] != Token.undefined and \
                    token[0] != Token.sign:
                tempPhrase[token[0]] = token[1]
        i = i + 1
        activeMachines = False
    return output
