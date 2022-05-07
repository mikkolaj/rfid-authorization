from typing import Optional
from threading import Thread
from threading import Timer
import uuid

from client.networking.NetworkConfig import ROOT_TIMEOUT_SECONDS
from client.networking.NetworkHandler import NetworkHandler
from client.networking.messages.DbSnapshotRequest import DbSnapshotRequest
from client.networking.messages.DbUpdateMessage import DbUpdateMessage
from client.networking.messages.ImAliveMessage import ImAliveMessage


class Host(Thread):
    def __init__(self) -> None:
        super().__init__()
        self.root_address: Optional[str] = None
        self.root_mac: Optional[int] = None
        self.mac = uuid.getnode()
        self.network_handler = NetworkHandler()

    def run(self):
        self.connect()

    def connect(self):
        interpreter = Thread(target=self.interpret_message)
        r = Timer(ROOT_TIMEOUT_SECONDS, self.set_root)
        """
        sł
        """

    def interpret_message(self) -> None:
        message = self.network_handler.receive_multicast_message()
        message.accept(self)

    def handle_im_alive(self, message: ImAliveMessage) -> None:
        if self.root_mac is None or message.mac < self.root_mac:
            self.root_mac = message.mac
            self.root_address = message.sender

    def handle_db_snapshot_request(self, db_snapshot_request: DbSnapshotRequest) -> None:
        pass

    def handle_db_update_message(self, db_update_message: DbUpdateMessage) -> None:
        pass

    def compare_mac(self):
        pass

    def set_root(self):
        self.compare_mac(self.best_mac, self.mac)
#         I COS TAM SE DALEJ
