from lr_parser.RuleTable import Rule
from lr_parser.parser_gen.MarkedRule import MarkedRule


class StateSet:
    def __init__(self, init_items: list[MarkedRule]):
        self.init_items: list[MarkedRule] = init_items
        self.state = set()  # Set of rules
        self.processed_nt = set()  # Set of non terminals which productions already added to set

    def get_unfolding(self, item: MarkedRule, rules: dict[str, list[Rule]]) -> list[MarkedRule]:
        unfolding = list()
        if not item.is_end_form():
            if item.is_next_non_terminal():
                non_term = item.get_marked_item().name
                if non_term not in self.processed_nt:
                    self.processed_nt.add(non_term)
                    unfolding.extend(self.get_productions_for_nt(non_term, rules))
        return unfolding

    def get_productions_for_nt(self, non_term: str, rules: dict[str, list[Rule]]) -> list[MarkedRule]:
        res = list()
        if non_term in rules:
            for rule in rules[non_term]:
                res.append(MarkedRule(rule))
        return res

    def generate_closure(self, rules: dict[str, list[Rule]]) -> list['StateSet']:
        """
        Generate closure for given start rules. Algorithm: 1. Recursively add rules to closure with production head
        equal to marked non terminal in rules that already in closure. 2. Group rules by marked non terminal. Generate
        state set for each group (successors).

        :param rules: list if grammar rules
        :return: list of
        """
        new_items = self.init_items
        while True:
            temp = list()
            for item in new_items:
                temp.extend(self.get_unfolding(item, rules))
                self.state.add(item)
            if temp:
                new_items = temp
            else:
                break

        return list()
