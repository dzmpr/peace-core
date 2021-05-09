from typing import Generic, TypeVar


T = TypeVar('T')


class Stack(Generic[T]):
    def __init__(self, init_value: T = None):
        self.stack: list[T] = list()
        if init_value is not None:
            self.stack.append(init_value)

    def __repr__(self):
        size = len(self.stack)
        if size == 0:
            return "Size: 0"
        else:
            return f"Size: {size}, top: {self.stack[-1]}"

    def push(self, value: T):
        self.stack.append(value)

    def top(self) -> T:
        return self.stack[-1]

    def pop(self) -> T:
        return self.stack.pop()

    def pop_num(self, size: int) -> list[T]:
        res: list[T] = list()
        for i in range(size):
            res.append(self.stack.pop())
        res.reverse()
        return res
