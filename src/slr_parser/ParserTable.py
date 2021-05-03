from slr_parser.Action import Action, ActionType


class ParserTable:
    def __init__(self, raw_actions: dict):
        self.table: dict[tuple[int, str], Action] = dict()
        self._fill_table(raw_actions)

    def __repr__(self):
        return f"Actions: {len(self.table)}"

    def _fill_table(self, raw_actions: dict):
        for raw_action in raw_actions:
            key = (raw_action["state"], raw_action["action_symbol"])
            action = Action(ActionType[raw_action["action"]], raw_action["value"])
            if key not in self.table:
                self.table[key] = action
            else:
                raise Exception(f"Actions conflict. Key {key}, a1: {self.table[key]}, a2: {action}.")

    def get_action(self, key: tuple[int, str]) -> Action:
        if key in self.table:
            action = self.table[key]
            if action.action_type != ActionType.ACTION_TRANSFER:
                return action
            else:
                raise Exception(f"Expected action, found transfer for key: {key}.")
        return Action.get_error_action()

    def get_transfer_action(self, key: tuple[int, str]) -> Action:
        if key in self.table:
            action = self.table[key]
            if action.action_type == ActionType.ACTION_TRANSFER:
                return action
            else:
                raise Exception(f"Expected transfer, found action for key: {key}.")
        return Action.get_error_action()
