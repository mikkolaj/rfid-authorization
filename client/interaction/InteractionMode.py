from enum import Enum


class InteractionMode(Enum):
    NO_ACTION = 0
    WRITE = 1
    READ = 2

    def __str__(self):
        return str(self.value)
