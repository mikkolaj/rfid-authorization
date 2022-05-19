from typing import List

from client.networking.messages.Message import Message
from client.persistance.types.User import User


class DbUpdateMessage(Message):
    def __init__(self, db_records: List[User]) -> None:
        super().__init__()
        self.db_records = db_records

    def accept(self, host) -> None:
        host.handle_db_update_message(self)
