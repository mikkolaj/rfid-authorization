from client.networking.messages.Message import Message


class ImAliveMessage(Message):
    def __init__(self, mac: int):
        super().__init__()
        self.mac = mac

    def __str__(self):
        return str(f"ImAliveMessage - Mac: {self.mac}")

    def accept(self, host) -> None:
        host.handle_im_alive(self)
