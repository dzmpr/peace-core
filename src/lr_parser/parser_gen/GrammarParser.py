from pathlib import Path
from lr_parser.RuleTable import Rule
from lexer.token import TokenClass
import sys


class NonTerminal:
    def __init__(self, name: str):
        self.name: str = name

    def __repr__(self):
        return self.name


class GrammarParser:
    def __init__(self):
        self.terminals_list = set()
        self.nonterminals_list = set()
        self.rules: list[Rule] = list()

        self.grammar_terminals = [
            TokenClass.word,
            TokenClass.colon,
            TokenClass.b_op,
            TokenClass.b_cl,
            TokenClass.hash,
            TokenClass.cb_cl,
            TokenClass.cb_op,
            TokenClass.newline
        ]

    def generate_from_file(self, path: Path):
        if not path.exists():
            print(f"File {path} not exists.", file=sys.stderr)
            return

        with open(path, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    self._parse_complex_rule(line)

        print(self.terminals_list)
        print(self.nonterminals_list)
        self.print_rules()

    def generate_from_str(self, grammar: str):
        for line in grammar.splitlines():
            line = line.strip()
            if line:
                self._parse_complex_rule(line)

        print(self.terminals_list)
        print(self.nonterminals_list)
        self.print_rules()

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
        self.nonterminals_list.add(production_head)

        # Split production trail to process each form
        production_forms = production_trail.split("|")
        for production_form in production_forms:
            self._parse_rule(production_head, production_form)

    def _parse_rule(self, production_head: str, production_body: str):
        raw_body = production_body.split(" ")
        production_body = list()
        for body_item in raw_body:
            # Skip empty strings
            if not body_item:
                continue

            # Remove unnecessary chars in item
            body_item = body_item.strip()
            # If item is terminal (all lower letters)
            if body_item.islower():
                term = TokenClass.from_str(body_item)
                # Check that terminal is in out grammar
                if term not in self.grammar_terminals:
                    raise Exception(f"Unknown terminal {body_item}.")

                production_body.append(term)
                self.terminals_list.add(term)
            else:
                production_body.append(self.get_non_terminal(body_item))
        rule = self.get_rule(production_head, production_body)
        self.rules.append(rule)

    def get_rule(self, production_head: str, production_body: list[TokenClass]) -> Rule:
        return Rule(production_head, production_body)

    def get_non_terminal(self, name: str) -> NonTerminal:
        return NonTerminal(name)

    def print_rules(self):
        for rule in self.rules:
            print(rule)
