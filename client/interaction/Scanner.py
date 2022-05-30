from posixpath import isabs
from threading import Thread
from time import sleep
from client.interaction.Door import Door

from client.interaction.InteractionMode import InteractionMode
from client.interaction.Placement import Placement
from client.networking.Host import Host
from client.persistance.Authorization import Authorization
from client.persistance.EventType import EventType
from client.persistance.DatabaseManager import DatabaseManager
from client.persistance.types.User import User
from rfid_library import SimpleMFRC522
from logging import info, debug


class Scanner(Thread):
    def __init__(self, placement: Placement, host: Host, door: Door, database_manager: DatabaseManager):
        super().__init__()
        self.database_manager = database_manager
        debug(f"Initializing scanner {placement}")
        self.board = SimpleMFRC522(bus=0, device=placement.value)
        debug(f"Scanner {placement} initialized")
        self.mode = InteractionMode.NO_ACTION
        self.placement = placement
        self.host = host
        self.door = door

    def run(self):
        info(f"Scanner {self.placement} started")
        while True:
            tag_id = self.board.read()[0]
            info(tag_id)
            user = self.database_manager.get_user(tag_id)
            is_authorized = Authorization.UNAUTHORIZED if user is None else user.is_authorized
            if self.mode == InteractionMode.READ:
                if is_authorized == Authorization.UNAUTHORIZED:
                    self.handle_unauthorized_user(tag_id)
                elif is_authorized == Authorization.AUTHORIZED:
                    self.handle_authorized_user(tag_id)
                elif is_authorized == Authorization.ADMIN:
                    self.handle_admin_user()

            elif self.mode == InteractionMode.WRITE:
                new_authorization = Authorization.AUTHORIZED if is_authorized == Authorization.UNAUTHORIZED else Authorization.UNAUTHORIZED
                self.handle_modify_user(new_authorization, tag_id)

            sleep(2)

    def set_interaction_mode(self, mode: InteractionMode):
        self.mode = mode

    def handle_unauthorized_user(self, tag_id: int):
        info("Unauthorized!!")
        event = EventType.DENIED_ENTRANCE if self.is_entrance() else EventType.DENIED_LEAVE
        self.database_manager.create_log(tag_id, event)

    def handle_authorized_user(self, tag_id: int):
        self.door.open()
        event = EventType.AUTHORIZED_ENTRANCE if self.is_entrance(
        ) else EventType.AUTHORIZED_LEAVE
        self.database_manager.create_log(tag_id, event)
        sleep(3)
        self.door.close()

    def handle_admin_user(self):
        info("YOU ARE THE ADMINISTRATOR!!")
        print("\n")
        self.database_manager.print_users()
        print("\n")
        self.database_manager.print_logs()
        print("\n")
        self.set_interaction_mode(InteractionMode.WRITE)

    def handle_modify_user(self, is_authorized: Authorization, tag_id: int):
        info("Adding user!!" if is_authorized ==
             Authorization.AUTHORIZED else "Removing user rights!!")

        self.database_manager.create_or_update_user(
            tag_id, is_authorized)
        self.host.send_one_user_update_to_root(tag_id)
        self.set_interaction_mode(InteractionMode.READ)

    def is_entrance(self):
        return self.placement == Placement.ENTRANCE
