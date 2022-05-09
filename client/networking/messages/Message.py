from typing import Optional

from client.networking.Host import Host


class Message:
    def __init__(self) -> None:
        self.sender: Optional[str] = None

    def accept(self, host: Host) -> None:
        pass
