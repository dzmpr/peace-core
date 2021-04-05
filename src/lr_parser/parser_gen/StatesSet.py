from lr_parser.RuleTable import Rule
from lr_parser.parser_gen.MarkedRule import MarkedRule
from lr_parser.parser_gen.LRSet import LRSet


class StatesSet:
    def __init__(self):
        self.closures: list[LRSet] = list()
        self.rules: list[Rule] = list()
        self.rules_dict: dict[str, list[Rule]] = dict()
        self.expanded_rules: list[MarkedRule] = list()

    def __str__(self):
        res = str()
        for item in self.closures:
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
        initial_state = LRSet([init_item])
        new_states: list[LRSet] = [initial_state]
        generated_states = True
        while generated_states:
            temp: list[LRSet] = list()
            for state in new_states:
                successors = state.generate_closure(self.rules_dict)
                if not self.is_state_in_set(state):
                    self.closures.append(state)
                    temp.extend(successors)

            if temp:
                new_states = temp
            else:
                generated_states = False

    def is_state_in_set(self, new_state: LRSet) -> bool:
        for state in self.closures:
            if state.state == new_state.state:
                return True
        return False
