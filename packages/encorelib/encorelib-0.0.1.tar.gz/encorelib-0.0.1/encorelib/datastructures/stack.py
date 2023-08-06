

class Stack(object):
    def __init__(self) -> None:
        self.data = []

    def push(self, obj) -> None:
        self.data.append(obj)

    def pop(self):
        return self.data.pop()

    def is_empty(self) -> bool:
        if len(self.data) == 0:
            return True
        return False

    def top(self) -> int:
        return len(self.data)

    def __repr__(self) -> str:
        return f'Stack({self.top()})'
