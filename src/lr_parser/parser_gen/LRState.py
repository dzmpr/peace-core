from lr_parser.RuleTable import Rule
from lr_parser.parser_gen.MarkedRule import MarkedRule
from lr_parser.parser_gen.RawAction import RawAction
from lr_parser.parser_gen.NonTerminal import NonTerminal
from lr_parser.parser_gen.Terminal import Terminal
from lr_parser.ActionTable import ActionType
from typing import Union, Optional


class LRState:
    def __init__(self, init_items: list[MarkedRule], state_id: int = None, parent_id: int = None):
        # Set of state rules
        self.state: set[MarkedRule] = set()
        # Start items list
        self.init_items: list[MarkedRule] = init_items
        # Set of non terminals which productions already added to state set
        self.processed_nt: set[NonTerminal] = set()
        # List of raw actions for this state
        self.raw_actions: list[RawAction] = list()

        self.state_id: int = state_id
        self.parents_id: set[int] = {parent_id}

    def __repr__(self):
        return f"Set size: {len(self.state)}"

    def __str__(self):
        res = f"State id - {self.state_id}. State parents: {self.parents_id}.\n"
        for item in self.state:
            res += str(item) + "\n"
        return res

    def __hash__(self):
        items = [hash(item) for item in self.state]
        items.sort()
        return hash(tuple(items))

    def set_id(self, state_id: int):
        self.state_id = state_id

    def add_parent_id(self, parent_id: int):
        self.parents_id.add(parent_id)

    def get_unfolding(self, item: MarkedRule, rules: dict[NonTerminal, list[Rule]]) -> list[MarkedRule]:
        unfolding = list()
        if not item.is_end_form():
            if item.is_next_non_terminal():
                non_term = item.get_marked_item()
                if non_term not in self.processed_nt:
                    self.processed_nt.add(non_term)
                    unfolding.extend(self.get_productions_for_nt(non_term, rules))
        return unfolding

    @staticmethod
    def get_productions_for_nt(non_term: NonTerminal, rules: dict[NonTerminal, list[Rule]]) -> list[MarkedRule]:
        res = list()
        if non_term in rules:
            for rule in rules[non_term]:
                res.append(MarkedRule(rule))
        return res

    def generate_closure(self, rules: dict[NonTerminal, list[Rule]]):
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

    def generate_successors(self, rules: dict[NonTerminal, list[Rule]]) -> list['LRState']:
        successors_list = list()
        groups = self.generate_groups()
        for group in groups:
            new_set = LRState(groups[group], parent_id=self.state_id)
            new_set.generate_closure(rules)
            successors_list.append(new_set)
            self._generate_shift_transfer(group, hash(new_set))
        self._generate_accept_reduce()
        return successors_list

    def _generate_shift_transfer(self, group: Union[Terminal, NonTerminal], target_hash: int):
        action: Optional[RawAction] = None
        if group.is_terminal():
            # If marked item is terminal - create shift action
            action = RawAction(ActionType.ACTION_SHIFT, self.state_id, group, target_hash)
        elif group.is_nonterminal():
            # If marked item is nonterminal - create transfer action
            action = RawAction(ActionType.ACTION_TRANSFER, self.state_id, group, target_hash)
        self.raw_actions.append(action)

    def _generate_accept_reduce(self):
        for item in self.state:
            if item.is_end_form():
                if item.rule.rule_id == 1:
                    # Action for augmented production in grammar
                    action = RawAction(ActionType.ACTION_ACCEPT, self.state_id, Terminal("$"), 0)
                else:
                    # Reduce action for other productions
                    action = RawAction(ActionType.ACTION_REDUCE, self.state_id, Terminal("$"), item.rule.rule_id)
                self.raw_actions.append(action)

    def generate_groups(self) -> dict[Union[Terminal, NonTerminal], list[MarkedRule]]:
        groups = dict()
        # For each item is state set
        for item in self.state:
            # If item is not in final form
            if not item.is_end_form():
                # Get marked item
                marker = item.get_marked_item()
                if marker in groups:
                    groups[marker].append(item.get_moved_marker())
                else:
                    groups[marker] = [item.get_moved_marker()]
        return groups
