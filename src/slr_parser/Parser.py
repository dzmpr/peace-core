from slr_parser.Action import ActionType
from slr_parser.ParserTable import ParserTable
from slr_parser.RuleTable import RuleTable
from slr_parser.Token import Token
from slr_parser.Stack import Stack


class Parser:
    def __init__(self, grammar: dict):
        self.stack: Stack = Stack()
        # Check is grammar in expected representation
        fields = {"actions", "rules", "terminals", "nonterminals", "start_nonterminal",
                  "augmented_nonterminal", "epsilon_terminal", "eof_terminal"}
        if fields - grammar.keys():
            raise Exception("Wrong grammar representation.")
        self.parser_table = ParserTable(grammar["actions"])
        self.rule_table: RuleTable = RuleTable(grammar["rules"], grammar["epsilon_terminal"])

    def __repr__(self):
        return f"State: {self.stack.top()}"

    def parse_input(self, token_list: list[Token]) -> list:
        current_token = 0
        token = token_list[0]
        accepted = False
        self.stack.push(0)

        # TODO:  remove
        res = list()
        #

        while not accepted:
            stack_top: int = self.stack.top()
            action = self.parser_table.get_action((stack_top, token.token_value))
            if action.action_type == ActionType.ACTION_ACCEPT:
                accepted = True
            elif action.action_type == ActionType.ACTION_ERROR:
                print("ERRRORRRERER")
                break
            elif action.action_type == ActionType.ACTION_SHIFT:
                self.stack.push(token)
                self.stack.push(action.value)
                current_token += 1
                token = token_list[current_token]
            elif action.action_type == ActionType.ACTION_REDUCE:
                rule = self.rule_table.get_rule(action.value)
                chain = self.stack.pop_num(len(rule.chain) * 2)
                state = self.stack.top()
                self.stack.push(rule.head)
                self.stack.push(self.parser_table.get_transfer_action((state, rule.head)).value)

                # TODO: remove
                res.append(f"{rule.head} {rule.rule_id}")
                #
            else:
                raise Exception(f"Unsupported action type {action.action_type}.")
        return res
