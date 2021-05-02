from typing import Union, Optional

from lr_parser.RuleTable import Rule
from lr_parser.parser_gen.Terminal import Terminal
from lr_parser.parser_gen.NonTerminal import NonTerminal


class FFSetGenerator:
    def __init__(self):
        # List of grammar rules
        self.rules_list: list[Rule] = list()
        self.rules_dict: dict[NonTerminal, list[Rule]] = dict()
        # Dict with calculated FIRSTs
        self.first_dict: dict[Union[Terminal, NonTerminal], set[Terminal]] = dict()
        # Dict with calculated FOLLOWs
        self.follow_dict: dict[NonTerminal, set[Terminal]] = dict()
        # Set of nonterminals
        self.nonterminals_set: set[NonTerminal] = set()
        # Set of terminals
        self.terminals_set: set[Terminal] = set()
        # Contains dict
        self.contains_dict: dict[NonTerminal, list[Rule]] = dict()
        # Start symbol
        self.start_symbol: Optional[NonTerminal] = None

    def set_rules(self, rules: list[Rule], rules_dict: dict[NonTerminal, list[Rule]]):
        self.rules_list = rules
        self.rules_dict = rules_dict
        self._prepare_rules()

    def _prepare_rules(self):
        # Process each rule
        for rule in self.rules_list:
            # Add rule head to nonterminals set
            self.nonterminals_set.add(rule.head)
            # Fill follow set for start nonterminal with EOF terminal
            if rule.rule_id == 1:
                self.follow_dict[rule.head] = {Terminal.get_eof()}
                self.start_symbol = rule.head

            # Check each symbol in production
            for symbol in rule.chain:
                if symbol.is_terminal():
                    # Add terminal to terminals set
                    self.terminals_set.add(symbol)
                else:
                    # Add nonterminal from rule body to set
                    self.nonterminals_set.add(symbol)

                    # Fill contains dict
                    if symbol not in self.contains_dict:
                        self.contains_dict[symbol] = [rule]
                    else:
                        self.contains_dict[symbol].append(rule)

    def calculate_sets(self):
        if not self.rules_list:
            raise Exception("Rules should be provided.")

        self._calculate_first_set()
        self._calculate_follow_set()

    def _calculate_first_set(self):
        # FIRST(x) = setOf(x), where x - terminal
        for terminal in self.terminals_set:
            self.first_dict[terminal] = {terminal}

        # Init FIRST(X) of nonterminal as empty set
        for nonterminal in self.nonterminals_set:
            self.first_dict[nonterminal] = set()

        first_size_before_iteration = 0
        first_size_after_iteration = self.__get_first_size()
        while first_size_after_iteration != first_size_before_iteration:
            first_size_before_iteration = first_size_after_iteration
            for nonterminal in self.nonterminals_set:
                first_set = set()
                for production in self.rules_dict[nonterminal]:
                    first_set |= self._generate_first_for_rule(production)
                self.first_dict[nonterminal] |= first_set

            first_size_after_iteration = self.__get_first_size()

    def _generate_first_for_rule(self, rule: Rule) -> set[Terminal]:
        epsilon = Terminal.get_epsilon()
        # FIRST set for production
        first_set: set[Terminal] = set()

        if len(rule.chain) == 1 and rule.chain[0] == epsilon:
            return {epsilon}

        for symbol in rule.chain:
            symbol_first_set = self.first_dict[symbol].copy()
            if epsilon not in symbol_first_set:
                first_set |= symbol_first_set
                break
            symbol_first_set.discard(epsilon)
            first_set |= symbol_first_set

        return first_set

    def _calculate_follow_set(self):
        # Init FOLLOW(X) as empty set
        for nonterminal in self.nonterminals_set:
            self.follow_dict[nonterminal] = set()
        # Start symbol FOLLOW contains $ (EOF)
        self.follow_dict[self.start_symbol] |= {Terminal.get_eof()}

        follow_size_before_iteration = 0
        follow_size_after_iteration = self.__get_follow_size()
        while follow_size_after_iteration != follow_size_before_iteration:
            follow_size_before_iteration = follow_size_after_iteration
            for nonterminal in self.nonterminals_set:
                if nonterminal == self.start_symbol:
                    continue

                follow_set: set[Terminal] = set()
                for rule in self.contains_dict[nonterminal]:
                    follow_set |= self._generate_follow_for_rule(nonterminal, rule)
                self.follow_dict[nonterminal] |= follow_set

            follow_size_after_iteration = self.__get_follow_size()

    def _generate_follow_for_rule(self, followable_nonterminal: NonTerminal, rule: Rule) -> set[Terminal]:
        rule_follow_set: set[Terminal] = set()
        if rule.chain[-1] == followable_nonterminal:
            rule_follow_set |= self.follow_dict[rule.head]
            return rule_follow_set

        epsilon = Terminal.get_epsilon()
        rule_chain = reversed(rule.chain)
        for symbol in rule_chain:
            if symbol == followable_nonterminal:
                rule_follow_set |= self.follow_dict[rule.head]
                return rule_follow_set

            first_set = self.first_dict[symbol].copy()
            if epsilon in first_set:
                first_set.discard(epsilon)
                rule_follow_set |= first_set
            else:
                rule_follow_set |= first_set
                return rule_follow_set
        return rule_follow_set

    def get_support_functions(self) -> tuple[dict, dict]:
        return self.first_dict, self.follow_dict

    def __get_first_size(self) -> int:
        size = 0
        for first_set in self.first_dict.values():
            size += len(first_set)
        return size

    def __get_follow_size(self) -> int:
        size = 0
        for follow_set in self.follow_dict.values():
            size += len(follow_set)
        return size
