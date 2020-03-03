from src.lexer.StateMachine import State
from src.lexer.lexer import Token
from src.syntaxer.SyntaxerStateMachine import SyntaxerStateMachine
from src.syntaxer.SyntaxerStateMachine import Phrase
from src.syntaxer import rules


class SyntaxerError(Exception):
    def __init__(self, expectedPhrase, atLine):
        self.expectedPhrase = expectedPhrase
        self.atLine = atLine


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

commentMachine = SyntaxerStateMachine(Phrase.comment, State.comment, {
    State.begin: rules.commentStart,
    State.comment: rules.commentEnd,
})

bodyMachine = SyntaxerStateMachine(Phrase.body, State.body, {
    State.begin: rules.bodyStart,
    State.body: rules.body
})

deviceMachine = SyntaxerStateMachine(Phrase.device, State.device, {
    State.begin: rules.deviceStart,
    State.deviceStart: rules.deviceEnd,
    State.device: rules.device
})

blockCloseMachine = SyntaxerStateMachine(Phrase.blockClose, State.accoladeCloseSign, {
    State.begin: rules.accoladeStart,
    State.accoladeCloseSign: rules.accoladeEnd
})



machines = {
    operatorMachine,
    expressionMachine,
    commentMachine,
    bodyMachine,
    deviceMachine,
    blockCloseMachine
}


def processTokens(machines, tokens):
    output = []
    activeMachines = False
    machineFound = False
    i = 0
    tempPhrase = []
    linesProcessed = 1
    while i < len(tokens):
        token = tokens[i]

        if token[0] == Token.newline:
            linesProcessed = linesProcessed + 1

        for machine in machines:
            machine.processObject(token)
            if machine.state != State.undefined:
                activeMachines = True

        if not activeMachines:
            for machine in machines:
                if not machineFound and machine.sequenceRecognized():
                    output.append([machine.name, tempPhrase.copy()])
                    machineFound = True
                    tempPhrase.clear()

            if token[0] == Token.undefined:
                return output

            if not machineFound:
                for machine in machines:
                    if machine.prevState != State.undefined:
                        raise SyntaxerError(machine.name, linesProcessed)

            for machine in machines:
                machine.resetState()

            i = i - 1
            machineFound = False
        else:
            if token[0] != Token.space and \
                    token[0] != Token.newline and \
                    token[0] != Token.undefined and \
                    token[0] != Token.sign:
                tempPhrase.append(token)

        i = i + 1
        activeMachines = False

    return output
