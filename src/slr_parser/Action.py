from enum import Enum


class ActionType(Enum):
    ACTION_ACCEPT = 0
    ACTION_SHIFT = 1
    ACTION_REDUCE = 2
    ACTION_ERROR = 3
    ACTION_TRANSFER = 4


class Action:
    def __init__(self, action_type: ActionType, value: int):
        self.action_type: ActionType = action_type
        self.value: int = value

    def __repr__(self):
        return f"{self.action_type.name}"

    @staticmethod
    def get_error_action() -> 'Action':
        return Action(ActionType.ACTION_ERROR, 0)