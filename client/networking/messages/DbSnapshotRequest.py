from client.networking.Host import Host


class DbSnapshotRequest:
    def __init__(self):
        super().__init__()

    def accept(self, host: Host) -> None:
        host.handle_db_snapshot_request(self)
