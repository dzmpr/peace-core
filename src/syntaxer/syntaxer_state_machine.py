from lexer.state_machine import State, StateMachine
from typing import Dict, Callable
from lexer.token import Token


class SyntaxerStateMachine(StateMachine):
    def __init__(self,
                 name,
                 success_state: State,
                 rules: Dict[State, Callable[[Token], State]]):
        super(SyntaxerStateMachine, self).__init__(name, rules)
        self.successState = success_state

    def process_object(self, obj: Token):
        self.prevState = self.state
        if self.state != State.undefined:
            self.state = self.rules[self.prevState](obj)

    def is_sequence_recognized(self):
        if self.prevState == self.successState:
            return True
        return False
