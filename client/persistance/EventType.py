from enum import Enum


class EventType(Enum):
    AUTHORIZED_ENTRANCE = 0
    DENIED_ENTRANCE = 1
    AUTHORIZED_LEAVE = 2
    DENIED_LEAVE = 3

    def __str__(self):
        return str(self.value)
