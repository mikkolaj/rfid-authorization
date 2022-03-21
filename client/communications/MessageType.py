from enum import Enum


class MessageType(Enum):
    IM_ALIVE = 1
    DB_UPDATE = 2
    HOST_ADVERTISEMENT = 3

