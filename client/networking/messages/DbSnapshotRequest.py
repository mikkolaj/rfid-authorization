from client.networking.messages.Message import Message


class DbSnapshotRequest(Message):
    def __init__(self):
        super().__init__()

    def accept(self, host) -> None:
        host.handle_db_snapshot_request(self)
