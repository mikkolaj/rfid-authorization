from datetime import datetime
from logging import debug, info
from random import randint
from threading import Thread, Event
from time import sleep
from typing import Optional
import uuid
import netifaces as ni

from client.networking.NetworkConfig import ROOT_TIMEOUT_SECONDS, IM_ALIVE_TIME_SECONDS
from client.networking.NetworkHandler import NetworkHandler
from client.networking.messages.DbSnapshotRequest import DbSnapshotRequest
from client.networking.messages.DbUpdateMessage import DbUpdateMessage
from client.networking.messages.ImAliveMessage import ImAliveMessage
from client.persistance.DatabaseManager import DatabaseManager
from client.persistance.types.User import User


class Host(Thread):
    def __init__(self, network_handler: NetworkHandler, database_manager: DatabaseManager) -> None:
        super().__init__()
        self.root_address: Optional[str] = None
        self.network_handler = network_handler
        self.database_manager = database_manager
        self.mac = uuid.getnode()
        self.root_mac: int = self.mac
        self.im_alive_update_time = None
        self.ip_address = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
        info("MAC:" + str(self.mac))

    def run(self):
        self.connect()

    def connect(self):
        message_interpreter = Thread(target=self.interpret_message)
        message_interpreter.start()
        sleep(ROOT_TIMEOUT_SECONDS)
        self.request_db_snapshot()
        root_thread = Thread(target=self.root_thread)
        root_thread.start()

    def interpret_message(self) -> None:
        while True:
            message = self.network_handler.receive_multicast_message()
            # print("Sender:", message.sender[0])
            # print("My address:", self.ip_address)
            if message.sender[0] != self.ip_address:
                message.accept(self)

    def handle_im_alive(self, message: ImAliveMessage) -> None:
        debug(f"Handling message {message}")
        self.im_alive_update_time = datetime.now()
        if message.mac < self.root_mac:
            self.root_mac = message.mac
            self.root_address = message.sender

    def handle_db_snapshot_request(self, message: DbSnapshotRequest) -> None:
        debug("Handling db snapshot message")
        users = self.database_manager.get_all_users()
        snapshot = DbUpdateMessage(users)

        self.network_handler.send_unicast_message(snapshot, message.sender)

    def handle_db_update_message(self, message: DbUpdateMessage) -> None:
        debug("Handling db update message")
        for user in message.db_records:
            current_user = self.database_manager.get_user(user.tag_id)
            print("dupa User: ", user)
            print("dupa Ten co mamy: ", current_user)

            if current_user is None or current_user.date < user.date:
                self.database_manager.create_or_update_user(
                    user.tag_id, user.is_authorized, user.date)
                if self.is_root():
                    self.network_handler.send_multicast_message(message)

    def root_thread(self):
        im_alive_message = ImAliveMessage(self.mac)
        ticker = Event()
        self.im_alive_update_time = datetime.now()
        while True:
            debug(f"Current root mac {self.root_mac}")
            if self.is_root():
                if not ticker.wait(IM_ALIVE_TIME_SECONDS):
                    self.network_handler.send_multicast_message(
                        im_alive_message)
            elif not ticker.wait(ROOT_TIMEOUT_SECONDS) and self.root_timeout_exceeded():
                debug("Root time exceeded - im the root now")
                self.root_mac = self.mac
                self.request_db_snapshot()

    def root_timeout_exceeded(self):
        delta = datetime.now() - self.im_alive_update_time
        return delta.seconds >= ROOT_TIMEOUT_SECONDS

    def is_root(self):
        return self.mac == self.root_mac

    def request_db_snapshot(self):
        message = DbSnapshotRequest()
        if self.is_root():
            self.network_handler.send_multicast_message(message)
        else:
            self.network_handler.send_unicast_message(
                message, self.root_address)
        debug("Db snapshot request sent")

    def send_one_user_update_to_root(self, tag_id: int):
        debug("Sending one user update to root!")
        user = self.database_manager.get_user(tag_id)
        message = DbUpdateMessage([user])

        if self.is_root():
            self.network_handler.send_multicast_message(message)
        else:
            self.network_handler.send_unicast_message(
                message, self.root_address)
