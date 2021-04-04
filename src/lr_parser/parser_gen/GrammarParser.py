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
                    self._parse_rule(line)
        print(self.terminals_list)
        print(self.nonterminals_list)
        self.print_rules()

    def generate_from_str(self, grammar: str):
        for line in grammar.splitlines():
            line = line.strip()
            if line:
                self._parse_rule(line)
        print(self.terminals_list)
        print(self.nonterminals_list)
        self.print_rules()

    def _parse_rule(self, line: str):
        production = line.split("->")
        if len(production) != 2:
            raise Exception("Unsupported production.")
        production[0] = production[0].strip()
        production[1] = production[1].strip()

        if not production[0].isupper():
            raise Exception("Right hand of production should contain non-terminal.")
        self.nonterminals_list.add(production[0])

        forms = production[1].split("|")
        for form in forms:
            raw_terminals = form.split(" ")
            production_body = list()
            for body_item in raw_terminals:
                if not body_item:
                    continue

                body_item = body_item.strip()
                if body_item.islower():
                    term = TokenClass.from_str(body_item)
                    if term not in self.grammar_terminals:
                        raise Exception(f"Unknown terminal {body_item}.")

                    production_body.append(term)
                    self.terminals_list.add(term)
                else:
                    production_body.append(self.get_non_terminal(body_item))
            self.rules.append(self.get_rule(production[0], production_body))

    def get_rule(self, production_head: str, production_body: list[TokenClass]) -> Rule:
        return Rule(production_head, production_body)

    def get_non_terminal(self, name: str) -> NonTerminal:
        return NonTerminal(name)

    def print_rules(self):
        for rule in self.rules:
            print(rule)