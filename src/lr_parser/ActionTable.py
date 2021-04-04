from enum import Enum
from lr_parser.Token import Token, TokenType


class ActionType(Enum):
    ACTION_ACCEPT = 0
    ACTION_SHIFT = 1
    ACTION_REDUCE = 2
    ACTION_ERROR = 3


class Action:
    def __init__(self, action_type: ActionType, value: int):
        self.action_type: ActionType = action_type
        self.value: int = value

    def __repr__(self):
        return f"{self.action_type.name}"


class ActionTable:
    def __init__(self):
        self.table: dict[int, dict[str, Action]] = {
            0: {
                "a": Action(ActionType.ACTION_SHIFT, 2),
                "b": Action(ActionType.ACTION_SHIFT, 3)
            },
            1: {
                "$": Action(ActionType.ACTION_ACCEPT, 0)
            },
            2: {
                "a": Action(ActionType.ACTION_SHIFT, 2),
                "b": Action(ActionType.ACTION_SHIFT, 3)
            },
            3: {
                "b": Action(ActionType.ACTION_REDUCE, 2),
                "$": Action(ActionType.ACTION_REDUCE, 2)
            },
            4: {
                "b": Action(ActionType.ACTION_SHIFT, 5)
            },
            5: {
                "b": Action(ActionType.ACTION_REDUCE, 1),
                "$": Action(ActionType.ACTION_REDUCE, 1)
            }
        }

    def get_action(self, state: int, terminal: str) -> Action:
        if state in self.table:
            if terminal in self.table[state]:
                return self.table[state][terminal]
        return Action(ActionType.ACTION_ERROR, 0)
