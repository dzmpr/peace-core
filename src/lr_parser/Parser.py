from lr_parser.ActionTable import ActionTable, ActionType
from lr_parser.TransferTable import TransferTable
from lr_parser.RuleTable import RuleTable
from lr_parser.Token import Token
from lr_parser.Stack import Stack


class Parser:
    def __init__(self, action_table: ActionTable, transfer_table: TransferTable, rule_table: RuleTable):
        self.stack: Stack = Stack()
        self.action_table: ActionTable = action_table
        self.transfer_table: TransferTable = transfer_table
        self.rule_table: RuleTable = rule_table

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
            action = self.action_table.get_action(stack_top, token.token_value)
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
                self.stack.push(rule.production)
                self.stack.push(self.transfer_table.get_state(state, rule.production))
                # TODO: remove
                res.append(rule.production)
                #
            else:
                raise Exception(f"Unsupported action type {action.action_type}.")
        return res
