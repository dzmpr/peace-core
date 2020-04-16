from enum import Enum


class State(Enum):
    def __repr__(self):
        return self.name

    undefined = 0
    begin = 1
    char = 2
    openBrace = 3
    space = 7
    num = 8
    sign = 9
    newline = 10
    tab = 11
    str_start = 12
    str_end = 13
    operator_end = 14
    parameter = 15
    parameter_end = 16
    keyword = 100
    firstWord = 101
    secondWord = 102
    equalSign = 104
    accoladeOpenSign = 105
    accoladeCloseSign = 106
    comment = 107
    body = 108
    blockStart = 109
    block = 110
    label = 111
    label_end = 112


class StateMachine:
    def __init__(self, name, rules):
        """
        State machine constructor.

        :param name: state machine token class
        :param rules: dict containing rules for machine
        """
        self.rules = rules
        self.name = name
        self.prevState = State.begin
        self.state = State.begin

    def __repr__(self):
        return f"{self.name.name}: {self.state.name}"

    def process_object(self, obj):
        self.prevState = self.state
        if self.state != State.undefined:
            self.state = self.rules[self.prevState](obj)

    def reset_state(self):
        """
        Set begin state for machine.
        """
        self.prevState = State.begin
        self.state = State.begin
