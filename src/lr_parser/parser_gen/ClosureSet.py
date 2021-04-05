from lr_parser.RuleTable import Rule
from lr_parser.parser_gen.MarkedRule import MarkedRule
from lr_parser.parser_gen.StateSet import StateSet


class ClosureSet:
    def __init__(self):
        self.closures = list()
        self.rules: list[Rule] = list()
        self.rules_dict: dict[str, list[Rule]] = dict()
        self.expanded_rules: list[MarkedRule] = list()

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
        state_set = StateSet([init_item])
        state_set.generate_closure(self.rules_dict)
