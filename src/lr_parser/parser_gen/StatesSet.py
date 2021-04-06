from lr_parser.RuleTable import Rule
from lr_parser.parser_gen.MarkedRule import MarkedRule
from lr_parser.parser_gen.LRState import LRState
from lr_parser.parser_gen.NonTerminal import NonTerminal


class StatesSet:
    def __init__(self):
        self.states: list[LRState] = list()
        self.rules: list[Rule] = list()
        self.rules_dict: dict[NonTerminal, list[Rule]] = dict()
        self.expanded_rules: list[MarkedRule] = list()

    def __str__(self):
        res = str()
        for item in self.states:
            res += str(item) + "\n"
        return res

    def set_rules(self, rules: list[Rule]):
        self.rules = rules
        for rule in self.rules:
            if rule.head in self.rules_dict:
                self.rules_dict[rule.head].append(rule)
            else:
                self.rules_dict[rule.head] = [rule]
        # self.expand_rules()

    def expand_rules(self):
        for rule in self.rules:
            marked_rule = MarkedRule(rule)
            self.expanded_rules.append(marked_rule)
            while not marked_rule.is_end_form():
                marked_rule = marked_rule.get_moved_marker()
                self.expanded_rules.append(marked_rule)

    def generate_closures(self, init_item: MarkedRule):
        new_states: list[LRState] = [LRState([init_item])]
        generated_states = True
        next_state_id = 0
        while generated_states:
            temp: list[LRState] = list()
            for state in new_states:
                state.set_id(next_state_id)
                state.generate_closure(self.rules_dict)
                successors = state.generate_successors(self.rules_dict)
                if not self.is_state_in_set(state):
                    next_state_id += 1
                    self.states.append(state)
                    temp.extend(successors)
                else:
                    self.add_parent_to_state(state)

            if temp:
                new_states = temp
            else:
                generated_states = False

    def is_state_in_set(self, new_state: LRState) -> bool:
        for state in self.states:
            if state.state == new_state.state:
                return True
        return False

    def add_parent_to_state(self, new_state: LRState):
        for state in self.states:
            if state.state == new_state.state:
                state.add_parent_id(new_state.parents_id.pop())
                break
