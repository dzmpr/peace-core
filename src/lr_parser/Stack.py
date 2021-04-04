from typing import Union


class Stack:
    def __init__(self, init_value: object = None):
        self.stack = list()
        if init_value is not None:
            self.stack.append(init_value)

    def __repr__(self):
        size = len(self.stack)
        if size == 0:
            return "Size: 0"
        else:
            return f"Size: {size}, top: {self.stack[-1]}"

    def push(self, value: object):
        self.stack.append(value)

    def top(self) -> Union[int, object]:
        return self.stack[-1]

    def pop(self) -> object:
        return self.stack.pop()

    def pop_num(self, size: int) -> list[object]:
        res: list[object] = list()
        for i in range(size):
            res.append(self.stack.pop())
        res.reverse()
        return res
