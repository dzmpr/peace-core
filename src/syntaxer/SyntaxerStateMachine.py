from src.lexer.StateMachine import StateMachine
from src.lexer.StateMachine import State


class SyntaxerStateMachine(StateMachine):
    def __init__(self, name, success_state, rules):
        super(SyntaxerStateMachine, self).__init__(name, rules)
        self.successState = success_state

    def process_object(self, obj):
        self.prevState = self.state
        if self.state != State.undefined:
            self.state = self.rules[self.prevState](obj)

    def is_sequence_recognized(self):
        if self.prevState == self.successState:
            return True
        return False
