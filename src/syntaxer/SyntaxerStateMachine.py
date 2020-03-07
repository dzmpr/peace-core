from enum import Enum
from src.lexer.StateMachine import StateMachine
from src.lexer.StateMachine import State


class PhraseGroup(Enum):
    def __repr__(self):
        return self.name

    operator = 0
    expression = 1
    comment = 2
    blockClose = 3
    body = 4
    device = 5
    label = 6


class SyntaxerStateMachine(StateMachine):
    def __init__(self, name, success_state, rules):
        super(SyntaxerStateMachine, self).__init__(name, rules)
        self.successState = success_state

    def processObject(self, obj):
        self.prevState = self.state
        if self.state != State.undefined:
            self.state = self.rules[self.prevState](obj)

    def is_sequence_recognized(self):
        if self.prevState == self.successState:
            return True
        return False
