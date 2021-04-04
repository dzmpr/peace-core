from pathlib import Path
from lr_parser.RuleTable import Rule
import sys


class GrammarParser:
    def __init__(self):
        self.terminals_list = set()
        self.nonterminals_list = set()
        self.rules: list[Rule] = list()

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

    def generate_from_str(self, grammar: str):
        for line in grammar.splitlines():
            line = line.strip()
            if line:
                self._parse_rule(line)
        print(self.terminals_list)
        print(self.nonterminals_list)

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
            terminals_list = form.split(" ")
            for terminal in terminals_list:
                terminal = terminal.strip()
                if terminal.islower():
                    self.terminals_list.add(terminal)
