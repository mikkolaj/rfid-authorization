from enum import Enum


class Authorization(Enum):
    UNAUTHORIZED = 0
    AUTHORIZED = 1
    ADMIN = 2

    def __str__(self):
        return str(self.value)
