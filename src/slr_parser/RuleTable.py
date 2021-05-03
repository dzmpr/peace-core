class Rule:
    def __init__(self, head: str, body: list[str], rule_id: int):
        self.head: str = head
        self.chain: list[str] = body
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
        string = f"{self.head} -> {self.chain}"
        return string


class RuleTable:
    def __init__(self, raw_rules: dict, epsilon_terminal: str):
        self.table: dict[int, Rule] = dict()
        self._fill_rules(raw_rules, epsilon_terminal)

    def __repr__(self):
        return f"Rules: {len(self.table)}"

    def _fill_rules(self, raw_rules: dict, epsilon_terminal: str):
        for raw_rule in raw_rules:
            # If rule have epsilon body - set empty list
            body = raw_rule["body"]
            if len(body) == 1 and body[0] == epsilon_terminal:
                body = list()

            rule = Rule(raw_rule["head"], body, raw_rule["rule_id"])
            if rule.rule_id not in self.table:
                self.table[rule.rule_id] = rule
            else:
                raise Exception(f"Rule conflict, id:{rule.rule_id}. R1: {self.table[rule.rule_id]}, R2: {rule}")

    def get_rule(self, rule_key: int) -> Rule:
        if rule_key in self.table:
            return self.table[rule_key]
        else:
            raise Exception(f"Unknown rule {rule_key}.")
