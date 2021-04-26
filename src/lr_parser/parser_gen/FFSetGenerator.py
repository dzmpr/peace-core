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
        for item in self.terminals_set:
            self.first_dict[item] = {item}

        # Stack to track nonterminals
        stack = list()
        # X -> Y1 Y2 Y3 ... Yn
        # FIRST(X) = setOf(FIRST(Y1) + FIRST(Y2) +...) until each Yi contains epsilon
        for item in self.nonterminals_set:
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
                            first_set |= self._generate_first_for_rule(production, False)
                    else:
                        self.first_dict[current_nonterminal] = first_set
                        if stack:
                            current_nonterminal = stack.pop()
                        else:
                            break

    def _generate_first_for_rule(self, rule: Rule, has_loop: bool) -> set[Terminal]:
        epsilon = Terminal.get_epsilon()
        # FIRST set for production
        first_set: set[Terminal] = set()
        # Marker that will be True if all symbols have epsilon in their FIRSTs
        has_epsilon = True
        # Marker that turns true if production contain it's head
        loop = False
        for symbol in rule.chain:
            if symbol == rule.head:
                if has_loop:
                    return first_set
                loop = True
                continue

            symbol_set = self.first_dict[symbol]
            if epsilon not in symbol_set:
                has_epsilon = False
                first_set |= symbol_set
                break
            symbol_set.discard(epsilon)
            first_set |= symbol_set

        if has_epsilon:
            first_set.add(epsilon)
        elif loop:
            return self._generate_first_for_rule(rule, True)
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
                # If nonterminal FIRST doesn't contains `epsilon` - we reach end of production
                if epsilon not in self.first_dict[symbol]:
                    return None
            # If there is no calculated first for this nonterminal
            elif symbol == rule.head:
                continue
            else:
                return symbol
        return None

    def _calculate_follow_set(self):
        # Stack to track nonterminals
        stack = list()

        # Loop over each nonterminal in grammar
        for nonterminal in self.nonterminals_set:
            current_nonterminal = nonterminal
            # Calculate FOLLOW only if it's needed
            if nonterminal not in self.follow_dict:
                while True:
                    rules_list = self.contains_dict[current_nonterminal]
                    follow_set: set[Terminal] = set()
                    for rule in rules_list:
                        next_nonterminal = self._get_next_followable_nonterminal(current_nonterminal, rule)
                        if next_nonterminal:
                            stack.append(current_nonterminal)
                            current_nonterminal = next_nonterminal
                            break
                        else:
                            follow_set |= self._generate_follow_for_rule(current_nonterminal, rule)
                    else:
                        self.follow_dict[current_nonterminal] = follow_set
                        if stack:
                            current_nonterminal = stack.pop()
                        else:
                            break

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

            first_set = self.first_dict[symbol]
            if epsilon in first_set:
                first_set.discard(epsilon)
                rule_follow_set |= first_set
            else:
                rule_follow_set |= first_set
                return rule_follow_set
        return rule_follow_set

    # def _get_follow_for_nonterminal_conserved(self, nonterminal: NonTerminal) -> set[Terminal]:
    #     epsilon = Terminal.get_epsilon()
    #
    #     rules = list()
    #     for rule in self.rules_list:
    #         if nonterminal in rule.chain:
    #             rules.append(rule)
    #
    #     follow_set = set()
    #     for rule in rules:
    #         if rule.rule_id == 1:
    #             follow_set.add(Terminal.get_eof())
    #
    #         index = rule.chain.index(nonterminal)
    #         temp = set()
    #         for i in range(index, len(rule.chain)):
    #             temp |= self.first_dict[rule.chain[index]]
    #             follow_set |= temp
    #             if epsilon not in temp:
    #                 break
    #         else:
    #             follow_set |= self.follow_dict[rule.head]
    #             return follow_set
    #         follow_set.discard(epsilon)
    #     return follow_set

    def _get_next_followable_nonterminal(self, followable_nonterminal: NonTerminal, rule: Rule) -> Optional[NonTerminal]:
        # Handle situation A -> abB, where B is followable nonterminal
        if rule.chain[-1] == followable_nonterminal:
            if rule.head not in self.follow_dict:
                return rule.head
            else:
                return None

        epsilon = Terminal.get_epsilon()
        rule_chain = reversed(rule.chain)
        for symbol in rule_chain:
            if symbol == followable_nonterminal:
                if rule.head not in self.follow_dict:
                    return rule.head
                else:
                    return None
            if epsilon not in self.first_dict[symbol]:
                return None
