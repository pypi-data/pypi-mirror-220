import time


class Timer(object):
    def __init__(self):
        self.timer = {}

    def start(self, name: str) -> float:
        self.timer[name] = (time.time(), 0)
        return self.timer[name][0]

    def end(self, name: str) -> float:
        self.timer[name] = (self.timer[name][0], time.time())
        return self.timer[name][1]

    def __repr__(self) -> str:
        log = '-----<Timer>-----\n'
        for name in self.timer:
            log += f'[{name}]: {self.timer[name][1]-self.timer[name][0]:.7f}\n'
        return log
