class TransferTable:
    def __init__(self):
        self.table: dict[int, dict[str, int]] = {
            0: {
                "S": 1
            },
            2: {
                "S": 4
            }
        }

    def get_state(self, state: int, non_terminal: str) -> int:
        if state in self.table:
            if non_terminal in self.table[state]:
                return self.table[state][non_terminal]
        raise Exception(f"Unknown transfer state:{state}, nt:{non_terminal}.")