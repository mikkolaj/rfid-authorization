from client.networking.Host import Host
from client.networking.messages.Message import Message


class ImAliveMessage(Message):
    def __init__(self, mac: int):
        super().__init__()
        self.mac = mac

    def accept(self, host: Host) -> None:
        host.handle_im_alive(self)
