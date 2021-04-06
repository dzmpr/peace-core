from lr_parser.RuleTable import Rule
from lr_parser.parser_gen.NonTerminal import NonTerminal
from lexer.token import TokenClass
from typing import Union


class MarkedRule:
    def __init__(self, rule: Rule, marker_position: int = 0):
        """
        Create marked rule with initial state of marker on first position.
        E.g. for rule S -> a b will be generated marked rule S -> * a b

        :param rule: rule
        :param marker_position: specify marker position (default - start)
        """
        self.rule: Rule = rule
        if len(rule.chain) < marker_position or marker_position < 0:
            raise Exception(f"Bad position ({marker_position}) for rule {rule}.")
        self.marker_position: int = marker_position

    def __repr__(self):
        desc = f"{self.rule.head} -> "
        for index, item in enumerate(self.rule.chain):
            if index == self.marker_position:
                desc += " *"
            desc += f" {item.name}"
        if self.marker_position == len(self.rule.chain):
            desc += " *"
        return desc

    def __hash__(self):
        """
        Fast implementation of 'hash'. Limited to 10_000 rule items.

        :return: hash of rule
        """
        return self.rule.rule_id * 10000 + self.marker_position

    def __eq__(self, other):
        if isinstance(other, MarkedRule):
            return hash(self) == hash(other)
        return False

    def is_end_form(self) -> bool:
        """
        :return: return is marker on last position of rule.
        """
        return len(self.rule.chain) == self.marker_position

    def get_moved_marker(self) -> 'MarkedRule':
        """
        Return new marked rule.
        Need to check that current rule isn't in final form.

        :return: new rule with marker moved to one position forward.
        """
        res = MarkedRule(self.rule, self.marker_position + 1)
        return res

    def is_next_non_terminal(self) -> bool:
        """
        Returns is marked item in rule is NonTerminal.

        :return: true if marked item is NonTerminal
        """
        if len(self.rule.chain) != self.marker_position:
            return isinstance(self.rule.chain[self.marker_position], NonTerminal)
        return False

    def is_next_terminal(self) -> bool:
        """
        Returns is marked item in rule is terminal.

        :return: true if marked item is terminal
        """
        if len(self.rule.chain) != self.marker_position:
            return isinstance(self.rule.chain[self.marker_position], TokenClass)
        return False

    def get_marked_item(self) -> Union[TokenClass, NonTerminal]:
        """
        Return marked item. It could be either terminal or non terminal.
        Require to check that rule isn't in final form.

        :return: marked item (term or non term)
        """
        return self.rule.chain[self.marker_position]
