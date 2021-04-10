from typing import Union, Optional

from lr_parser.RuleTable import Rule
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
        self._generate_first()
        self._generate_follow()

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

    def _generate_first(self):
        # FIRST(x) = setOf(x), where x - terminal
        for item in self.terminals:
            self.first_dict[item] = {item}

        # Stack to track nonterminals
        stack = list()
        # X -> Y1 Y2 Y3 ... Yn
        # FIRST(X) = setOf(FIRST(Y1) + FIRST(Y2) +...) until each Yi contains epsilon
        for item in self.nonterminals:
            current_nonterminal = item
            # Generate FIRST only if needed
            if current_nonterminal not in self.first_dict:
                while True:
                    productions_list = self.rules_dict[current_nonterminal]
                    first_set = set()
                    for production in productions_list:
                        next_nonterminal = self._get_next_firstable_nonterminal(production)
                        if next_nonterminal:
                            # If we have nnt not None it means we should create FIRST for it
                            stack.append(current_nonterminal)
                            current_nonterminal = next_nonterminal
                            break
                        else:
                            first_set |= self._generate_first_for_rule(production)
                    else:
                        self.first_dict[current_nonterminal] = first_set
                        if stack:
                            current_nonterminal = stack.pop()
                        else:
                            break

    def _generate_first_for_rule(self, rule: Rule) -> set[Terminal]:
        epsilon = Terminal.get_epsilon()  # Epsilon terminal
        first_set: set[Terminal] = set()
        for symbol in rule.chain:
            symbol_set = self.first_dict[symbol]
            if epsilon not in symbol_set:
                first_set |= symbol_set
                break
            symbol_set.discard(epsilon)
            first_set |= symbol_set
        return first_set

    def _get_next_firstable_nonterminal(self, rule: Rule) -> Optional[NonTerminal]:
        epsilon = Terminal.get_epsilon()
        # Check every symbol in production
        for symbol in rule.chain:
            # If we reach terminal - nonterminal is FIRSTable
            if symbol.is_terminal():
                return None
            # If symbol is nonterminal
            elif symbol in self.first_dict:
                # If nonterminal FIRST contains `epsilon` - go to next iteration
                if epsilon in self.first_dict[symbol]:
                    continue
                # If nonterminal FIRST doesn't contains `epsilon` - we reach end of production
                else:
                    return None
            # If there is no calculated first for this nonterminal
            else:
                return symbol
        return None

    def _generate_follow(self):
        pass
