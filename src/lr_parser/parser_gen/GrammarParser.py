import sys
from pathlib import Path
from typing import Union

from lr_parser.RuleTable import Rule
from lr_parser.parser_gen.MarkedRule import MarkedRule
from lr_parser.parser_gen.NonTerminal import NonTerminal
from lr_parser.parser_gen.StatesSet import StatesSet
from lr_parser.parser_gen.Terminal import Terminal


class GrammarParser:
    def __init__(self, epsilon_name: str = Terminal.EPSILON, eof_output: str = Terminal.EOF):
        self.terminals_set: set[Terminal] = set()
        self.nonterminals_set: set[NonTerminal] = set()
        # Rule index var
        self.rule_count: int = 1
        # List of parsed rules
        self.rules: list[Rule] = list()
        self.parser_states = StatesSet()

        self.epsilon_name: str = epsilon_name
        Terminal.set_eof_output(eof_output)

    def generate_from_file(self, path: Path):
        if not path.exists():
            print(f"File {path} not exists.", file=sys.stderr)
            return

        with open(path, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    self._parse_complex_rule(line)

        self._process_grammar()

    def generate_from_str(self, grammar: str):
        for line in grammar.splitlines():
            line = line.strip()
            if line:
                self._parse_complex_rule(line)

        self._process_grammar()

    def _process_grammar(self):
        # Pass parsed rules to states generator
        self.parser_states.set_rules(self.rules)
        # Pass sets of terminals and nonterminals to states generator
        self.parser_states.set_symbols(self.terminals_set, self.nonterminals_set)
        # Let generate support functions for closures
        self.parser_states.generate_support_functions()

        self._build_closures()
        self._debug_output()

    def _parse_complex_rule(self, line: str):
        # Split left and right parts of production
        production = line.split("->")
        # Check is production input correct
        if len(production) != 2:
            raise Exception("Unsupported production.")

        production_head = production[0].strip()
        production_trail = production[1].strip()

        # Check that production head represented by non terminal
        if not production_head[0].isupper():
            raise Exception("Left hand of production should contain non-terminal.")
        production_head = NonTerminal(production_head)
        self.nonterminals_set.add(production_head)

        # Split production trail to process each form
        production_forms = production_trail.split("|")
        for production_form in production_forms:
            self._parse_rule(production_head, production_form)

    def _parse_rule(self, production_head: NonTerminal, production_body: str):
        raw_body = production_body.split(" ")
        production_body: list[Union[Terminal, NonTerminal]] = list()
        for body_item in raw_body:
            # Skip empty strings
            if not body_item:
                continue

            # Remove unnecessary chars in item
            body_item = body_item.strip()
            # If item is terminal
            if body_item.islower():
                if body_item == self.epsilon_name:
                    terminal = Terminal.get_epsilon()
                else:
                    terminal = Terminal(body_item)

                production_body.append(terminal)
                self.terminals_set.add(terminal)
            else:
                production_body.append(NonTerminal(body_item))

        rule = self.get_rule(production_head, production_body)
        self.rules.append(rule)

    def _build_closures(self):
        init_rule = self.rules[0]
        init_rule = MarkedRule(init_rule)
        self.parser_states.generate_closures(init_rule)

    def get_rule(self, production_head: NonTerminal, production_body: list[Union[Terminal, NonTerminal]]) -> Rule:
        rule = Rule(production_head, production_body, self.rule_count)
        self.rule_count += 1
        return rule

    def _debug_output(self):
        print(self.parser_states)
        print(f"Terminals: {self.terminals_set}")
        print(f"Nonterminals: {self.nonterminals_set}")
        self._debug_print_rules()
        self._debug_print_action()
        self._debug_print_support_functions()

    def _debug_print_rules(self):
        print("\nParsed rules:")
        for rule in self.rules:
            print(rule)

    def _debug_print_action(self):
        print("\nGenerated actions:")
        for action in self.parser_states.resolve_actions():
            print(action)

    def _debug_print_support_functions(self):
        (first, follow) = self.parser_states.get_support_functions()
        print("\nFirst sets:")
        for symbol, first_set in first.items():
            print(f"{symbol} : {first_set}")

        print("\nFollow sets:")
        for nonterminal, follow_set in follow.items():
            print(f"{nonterminal} : {follow_set}")
