from src.lexer import lexer


class StateMachine:
    def __init__(self, name, rules):
        self.state = lexer.states.begin
        self.prevState = lexer.states.begin
        self.rules = rules
        self.name = name

    def __str__(self):
        return self.name

    def processObject(self, obj):
        self.prevState = self.state
        if self.state != lexer.states.undefined:
            self.state = self.rules[self.prevState](obj)

    def resetState(self):
        self.prevState = lexer.states.begin
        self.state = lexer.states.begin
