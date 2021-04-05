from lr_parser.RuleTable import Rule
from lr_parser.parser_gen.MarkedRule import MarkedRule


class LRState:
    def __init__(self, init_items: list[MarkedRule], state_id: int = None, parent_id: int = None):
        self.init_items: list[MarkedRule] = init_items
        self.state: set[MarkedRule] = set()  # Set of rules
        self.processed_nt: set[str] = set()  # Set of non terminals which productions already added to set

        self.state_id: int = state_id
        self.parents_id: set[int] = {parent_id}

    def __repr__(self):
        return f"Set size: {len(self.state)}"

    def __str__(self):
        res = f"State {self.state_id} {self.parents_id}\n"
        for item in self.state:
            res += str(item) + "\n"
        return res

    def set_id(self, state_id: int):
        self.state_id = state_id

    def add_parent_id(self, parent_id: int):
        self.parents_id.add(parent_id)

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

    def generate_closure(self, rules: dict[str, list[Rule]]) -> list['LRState']:
        """
        Generate closure for given start rules. Algorithm: 1. Recursively add rules to closure with production head
        equal to marked non terminal in rules that already in closure. 2. Group rules by marked non terminal. Generate
        state set for each group (successors).

        :param rules: list if grammar rules
        :return: list of
        """
        successors_list = list()

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

        groups = self.generate_groups()
        for group in groups:
            successors_list.append(LRState(group, parent_id=self.state_id))

        return successors_list

    def generate_groups(self) -> list[list[MarkedRule]]:
        groups = dict()
        for item in self.state:
            if not item.is_end_form():
                marker = item.get_marked_item()
                if marker.name in groups:
                    groups[marker.name].append(item.get_moved_marker())
                else:
                    groups[marker.name] = [item.get_moved_marker()]
        return list(groups.values())
