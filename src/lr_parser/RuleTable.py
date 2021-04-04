from lexer.token import TokenClass


class Rule:
    def __init__(self, result, chain: list):
        self.production = result
        self.chain: list = chain

    def __repr__(self):
        return f"{self.production} -> {self.chain}"

    def __str__(self):
        string = f"{self.production} -> "
        for item in self.chain:
            string += item.name
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