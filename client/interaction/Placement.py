from enum import Enum


class Placement(Enum):
    ENTRANCE = 0
    EXIT = 1

    def __str__(self):
        return str(self.value)
