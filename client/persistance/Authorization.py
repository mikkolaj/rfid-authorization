from enum import Enum


class Authorization(Enum):
    UNAUTHORIZED = 0,
    AUTHORIZED = 1,
    ADMIN = 2,
