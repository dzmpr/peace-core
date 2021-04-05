from lexer.token import TokenClass


class Rule:
    def __init__(self, production_head: str, body: list, rule_id: int):
        self.head: str = production_head
        self.chain: list = body
        if rule_id <= 0:
            raise Exception("Rule identifier should be greater than 0.")
        self.rule_id: int = rule_id

    def __repr__(self):
        return f"{self.head} -> {self.chain}"

    def __str__(self):
        """
        Pretty print rule in form: HEAD -> I T E M S
        """
        string = f"{self.head} -> "
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
