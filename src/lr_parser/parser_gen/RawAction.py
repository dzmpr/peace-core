from lr_parser.ActionTable import Action, ActionType
from lr_parser.parser_gen.Terminal import Terminal
from lr_parser.parser_gen.NonTerminal import NonTerminal
from typing import Union


class RawAction(Action):
    def __init__(self,
                 action_type: ActionType,
                 state_id: int,
                 action_item: Union[Terminal, NonTerminal],
                 temp_value: int):
        super().__init__(action_type, 0)
        self.state_id: int = state_id
        self.action_item: Union[Terminal, NonTerminal] = action_item
        self.temp_value: int = temp_value

    def __repr__(self):
        return f"S:{self.state_id} C:{self.action_item.item_name}, {self.action_type}"

    def resolve_action(self, hashmap: dict[int, int]):
        if self.action_type == ActionType.ACTION_SHIFT or self.action_type == ActionType.ACTION_TRANSFER:
            self.value = hashmap[self.temp_value]
        else:
            self.value = self.temp_value
