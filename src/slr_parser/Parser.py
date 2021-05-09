import sys

from slr_parser.AbstractSyntaxTree import ASTNode
from slr_parser.Action import ActionType
from slr_parser.ParserTable import ParserTable
from slr_parser.RuleTable import RuleTable
from slr_parser.Token import Token
from slr_parser.Stack import Stack


class Parser:
    def __init__(self, grammar: dict):
        self.states_stack: Stack = Stack()
        self.prefix_stack: Stack = Stack()
        # Check is grammar in expected representation
        fields = {"actions", "rules", "terminals", "nonterminals", "start_nonterminal",
                  "augmented_nonterminal", "epsilon_terminal", "eof_terminal"}
        if fields - grammar.keys():
            raise Exception("Wrong grammar representation.")
        self.parser_table = ParserTable(grammar["actions"])
        self.rule_table: RuleTable = RuleTable(grammar["rules"], grammar["epsilon_terminal"])

    def __repr__(self):
        return f"State: {self.states_stack.top()}"

    def parse_input(self, token_list: list[Token]) -> ASTNode:
        current_token = 0
        token = token_list[0]
        accepted = False
        self.states_stack.push(0)

        while not accepted:
            stack_top: int = self.states_stack.top()
            action = self.parser_table.get_action((stack_top, token.token_value))
            if action.action_type == ActionType.ACTION_ACCEPT:
                accepted = True
            elif action.action_type == ActionType.ACTION_ERROR:
                print(f"ERROR! Unexpected token {token}.", file=sys.stderr)
                break
            elif action.action_type == ActionType.ACTION_SHIFT:
                self.prefix_stack.push(token)
                self.states_stack.push(action.value)
                current_token += 1
                token = token_list[current_token]
            elif action.action_type == ActionType.ACTION_REDUCE:
                rule = self.rule_table.get_rule(action.value)
                self.states_stack.pop_num(rule.body_len)
                chain = self.prefix_stack.pop_num(rule.body_len)
                state = self.states_stack.top()
                node = ASTNode(rule.head, chain)
                self.prefix_stack.push(node)
                self.states_stack.push(self.parser_table.get_transfer_action((state, rule.head)).value)
            else:
                raise Exception(f"Unsupported action type {action.action_type}.")
        return self.prefix_stack.top()
