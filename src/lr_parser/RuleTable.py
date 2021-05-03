from lr_parser.parser_gen.NonTerminal import NonTerminal
from lr_parser.parser_gen.Terminal import Terminal
from typing import Union


class Rule:
    def __init__(self, production_head: NonTerminal, body: list[Union[Terminal, NonTerminal]], rule_id: int):
        self.head: NonTerminal = production_head
        self.chain: list[Union[Terminal, NonTerminal]] = body
        if rule_id <= 0:
            raise Exception("Rule identifier should be greater than 0.")
        self.rule_id: int = rule_id

    def __repr__(self):
        return f"{self.head} -> {self.chain}"

    def __hash__(self) -> int:
        return hash(tuple([self.head, *self.chain]))

    def __eq__(self, other):
        if isinstance(other, Rule):
            return self.head == other.head and self.chain == other.chain
        return False

    def __str__(self):
        """
        Pretty print rule in form: HEAD -> I T E M S
        """
        string = f"{self.head} -> "
        for item in self.chain:
            string += item.item_name
            string += " "
        return string


class RuleTable:
    def __init__(self):
        self.table: dict[int, Rule] = dict()

    def add_rule(self, rule_key: int, rule: Rule):
        if rule_key not in self.table:
            self.table[rule_key] = rule
        else:
            raise Exception("Rule already exists.")

    def get_rule(self, rule_key: int) -> Rule:
        if rule_key in self.table:
            return self.table[rule_key]
        else:
            raise Exception(f"Unknown rule {rule_key}.")
