from client.networking.Host import Host
from client.networking.messages.Message import Message


class DbSnapshotRequest(Message):
    def __init__(self):
        super().__init__()

    def accept(self, host: Host) -> None:
        host.handle_db_snapshot_request(self)
