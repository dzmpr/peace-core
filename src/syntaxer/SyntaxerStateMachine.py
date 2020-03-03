from enum import Enum
from src.lexer.StateMachine import StateMachine
from src.lexer.StateMachine import State


class Phrase(Enum):
    def __repr__(self):
        return self.name

    operator = 0
    expression = 1
    comment = 2
    blockClose = 3
    body = 4
    device = 5


class SyntaxerStateMachine(StateMachine):
    def __init__(self, name, successState, rules):
        super(SyntaxerStateMachine, self).__init__(name, rules)
        self.successState = successState

    def processObject(self, obj):
        self.prevState = self.state
        if self.state != State.undefined:
            self.state = self.rules[self.prevState](obj)

    def sequenceRecognized(self):
        if self.prevState == self.successState:
            return True
        return False
