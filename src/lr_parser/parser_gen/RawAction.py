from lr_parser.ActionTable import Action, ActionType


class RawAction(Action):
    def __init__(self, action_type: ActionType, successor_hash: int):
        super().__init__(action_type, 0)
        self.successor_state_hash: int = successor_hash
