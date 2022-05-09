from typing import Optional
from threading import Thread
from threading import Timer
import uuid

from client.networking.NetworkConfig import ROOT_TIMEOUT_SECONDS
from client.networking.NetworkHandler import NetworkHandler
from client.networking.messages.DbSnapshotRequest import DbSnapshotRequest
from client.networking.messages.DbUpdateMessage import DbUpdateMessage
from client.networking.messages.ImAliveMessage import ImAliveMessage
from client.persistance.DatabaseManager import DatabaseManager


class Host(Thread):
    def __init__(self, network_handler: NetworkHandler, database_manager: DatabaseManager) -> None:
        super().__init__()
        self.root_address: Optional[str] = None
        self.root_mac: Optional[int] = None
        self.network_handler = network_handler
        self.database_manager = database_manager
        self.mac = uuid.getnode()

    def run(self):
        self.connect()

    def connect(self):
        interpreter = Thread(target=self.interpret_message)
        r = Timer(ROOT_TIMEOUT_SECONDS, self.set_root)

    def interpret_message(self) -> None:
        message = self.network_handler.receive_multicast_message()
        message.accept(self)

    def handle_im_alive(self, message: ImAliveMessage) -> None:
        if self.root_mac is None or message.mac < self.root_mac:
            self.root_mac = message.mac
            self.root_address = message.sender

    def handle_db_snapshot_request(self, message: DbSnapshotRequest) -> None:
        users = self.database_manager.get_all_users()
        snapshot = DbUpdateMessage(users)

        self.network_handler.send_unicast_message(snapshot, message.sender)

    def handle_db_update_message(self, message: DbUpdateMessage) -> None:
        for user in message.db_records:
            current_user = self.database_manager.get_user(user.tag_id)

            if current_user is None or current_user.date < user.date:
                self.database_manager.create_or_update_user(user.tag_id, user.is_authorized, user.date)

