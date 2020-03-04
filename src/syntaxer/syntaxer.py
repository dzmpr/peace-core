from src.lexer.StateMachine import State
from src.lexer.lexer import Token
from src.syntaxer.SyntaxerStateMachine import SyntaxerStateMachine
from src.syntaxer.SyntaxerStateMachine import Phrase
from src.syntaxer.SemanticProcessor import SemanticProcessor
from src.syntaxer.SemanticProcessor import SyntaxParseError
from src.syntaxer import rules

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
    phrase = []
    checker = SemanticProcessor()
    while i < len(tokens):
        token = tokens[i]

        # New line check
        if token[0] == Token.newline:
            checker.nextLine()

        # Process token
        for machine in machines:
            machine.processObject(token)
            if machine.state != State.undefined:
                activeMachines = True

        # Check machine states
        if not activeMachines:
            for machine in machines:
                if not machineFound and machine.sequenceRecognized():
                    phrase = [machine.name, tempPhrase.copy()]
                    output.append(phrase)
                    machineFound = True
                    tempPhrase.clear()
                    checker.processPhrase(phrase)

            if token[0] == Token.undefined:
                if not checker.isBlocksClosed():
                    raise SyntaxParseError("Syntax error. Bad scoping.")
                return output

            # Token wasn't recognized by any machine
            if not machineFound:
                for machine in machines:
                    if machine.prevState != State.undefined:
                        raise SyntaxParseError("Syntax error. Expected {} at line {}.".format(machine.name, checker.procesedLines()))

            # Reset machine states
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
