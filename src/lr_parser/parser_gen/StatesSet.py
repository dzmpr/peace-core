from typing import Union

from lr_parser.RuleTable import Rule
from lr_parser.parser_gen.FFSetGenerator import FFSetGenerator
from lr_parser.parser_gen.LRState import LRState
from lr_parser.parser_gen.MarkedRule import MarkedRule
from lr_parser.parser_gen.NonTerminal import NonTerminal
from lr_parser.parser_gen.RawAction import RawAction
from lr_parser.parser_gen.Terminal import Terminal


class StatesSet:
    def __init__(self):
        # List (`set`) of parser states
        self.states_list: list[LRState] = list()
        # List of grammar productions
        self.rules_list: list[Rule] = list()
        # Dict of productions grouped by head nonterminal
        self.rules_dict: dict[NonTerminal, list[Rule]] = dict()
        # Dict of FIRST(X) sets for each X in grammar
        self.first_dict: dict[Union[Terminal, NonTerminal], set[Terminal]] = dict()
        # Dict of FOLLOW(X) sets for each nonterminal X in grammar
        self.follow_dict: dict[NonTerminal, set[Terminal]] = dict()
        # Grammar symbols sets
        self.terminals: set[Terminal] = set()
        self.nonterminals: set[NonTerminal] = set()

        self.ff_generator: FFSetGenerator = FFSetGenerator()

    def __str__(self):
        res = str()
        for item in self.states_list:
            res += str(item) + "\n"
        return res

    def set_rules(self, rules: list[Rule]):
        self.rules_list = rules
        for rule in self.rules_list:
            if rule.head in self.rules_dict:
                self.rules_dict[rule.head].append(rule)
            else:
                self.rules_dict[rule.head] = [rule]

    def set_symbols(self, terminals: set[Terminal], nonterminals: set[NonTerminal]):
        self.terminals = terminals
        self.nonterminals = nonterminals

    def generate_support_functions(self):
        self.ff_generator.set_rules(self.rules_list, self.rules_dict)
        self.ff_generator.calculate_sets()

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
                    self.states_list.append(state)
                    temp.extend(successors)
                else:
                    self.add_parent_to_state(state)

            if temp:
                new_states = temp
            else:
                generated_states = False

    def _get_raw_actions(self) -> list[RawAction]:
        actions: list[RawAction] = list()
        for item in self.states_list:
            actions.extend(item.raw_actions)
        return actions

    def resolve_actions(self) -> list[RawAction]:
        hashmap = self.get_states_hashes()
        raw_actions = self._get_raw_actions()
        for raw_action in raw_actions:
            raw_action.resolve_action(hashmap)
        return raw_actions

    def get_states_hashes(self) -> dict[int, int]:
        result: dict[int, int] = dict()
        for item in self.states_list:
            result[hash(item)] = item.state_id
        return result

    def is_state_in_set(self, new_state: LRState) -> bool:
        for state in self.states_list:
            if state.state == new_state.state:
                return True
        return False

    def add_parent_to_state(self, new_state: LRState):
        for state in self.states_list:
            if state.state == new_state.state:
                state.add_parent_id(new_state.parents_id.pop())
                break
