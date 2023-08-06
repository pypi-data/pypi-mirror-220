import time


def ftime():
    return time.monotonic()


# TODO
class WriteId:
    def __init__(self):
        self._curent = 0
        self._reserve = 0

    @property
    def current(self):
        return self._curent

    def next(self):
        self._curent += 1
        return self._curent

    def reserve(self):
        self._reserve += 1
        return self._reserve

