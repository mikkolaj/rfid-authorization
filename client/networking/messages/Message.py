from typing import Optional


class Message:
    def __init__(self) -> None:
        self.sender: Optional[str] = None

    def accept(self, host) -> None:
        pass
