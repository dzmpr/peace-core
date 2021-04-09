from pathlib import Path
from lr_parser.RuleTable import Rule
from lr_parser.parser_gen.StatesSet import StatesSet
from lr_parser.parser_gen.MarkedRule import MarkedRule
from lr_parser.parser_gen.Terminal import Terminal
from lr_parser.parser_gen.NonTerminal import NonTerminal
from lr_parser.parser_gen.ProductionItem import ProductionItem
from typing import Union
import sys


class GrammarParser:
    def __init__(self):
        self.terminals_list: set[Terminal] = set()
        self.nonterminals_list: set[NonTerminal] = set()
        self.rules: list[Rule] = list()

        self.rule_count: int = 1

        self.grammar_terminals = [
            Terminal("word"),
            Terminal("colon"),
            Terminal("b_op"),
            Terminal("b_cl"),
            Terminal("hash"),
            Terminal("cb_cl"),
            Terminal("cb_op"),
            Terminal("newline")
            # TokenClass.word,
            # TokenClass.colon,
            # TokenClass.b_op,
            # TokenClass.b_cl,
            # TokenClass.hash,
            # TokenClass.cb_cl,
            # TokenClass.cb_op,
            # TokenClass.newline
        ]

        self.closures = StatesSet()

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
        self.closures.set_rules(self.rules)
        self._build_closures()
        print(self.closures)
        print(self.terminals_list)
        print(self.nonterminals_list)
        self._debug_print_rules()
        self._debug_print_action()

    def _parse_complex_rule(self, line: str):
        # Split left and right parts of production
        production = line.split("->")
        # Check is production input correct
        if len(production) != 2:
            raise Exception("Unsupported production.")

        production_head = production[0].strip()
        production_trail = production[1].strip()

        # Check that production head represented by non terminal
        if not production_head.isupper():
            raise Exception("Right hand of production should contain non-terminal.")
        production_head = NonTerminal(production_head)
        self.nonterminals_list.add(production_head)

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
            # If item is terminal (all lower letters)
            if body_item.islower():
                term = Terminal(body_item)
                # term = TokenClass.from_str(body_item)
                # Check that terminal is in out grammar
                if term not in self.grammar_terminals:
                    raise Exception(f"Unknown terminal {body_item}.")

                production_body.append(term)
                self.terminals_list.add(term)
            else:
                production_body.append(NonTerminal(body_item))

        rule = self.get_rule(production_head, production_body)
        self.rules.append(rule)

    def _build_closures(self):
        init_rule = self.rules[0]
        init_rule = MarkedRule(init_rule)
        self.closures.generate_closures(init_rule)

    def get_rule(self, production_head: NonTerminal, production_body: list[Union[Terminal, NonTerminal]]) -> Rule:
        rule = Rule(production_head, production_body, self.rule_count)
        self.rule_count += 1
        return rule

    def _debug_print_rules(self):
        for rule in self.rules:
            print(rule)

    def _debug_print_action(self):
        for action in self.closures.resolve_actions():
            print(action)
