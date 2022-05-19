from threading import Thread
from time import sleep

from client.interaction.InteractionMode import InteractionMode
from client.interaction.Placement import Placement
from client.persistance.Authorization import Authorization
from client.persistance.EventType import EventType
from client.persistance.DatabaseManager import DatabaseManager
from client.persistance.types.User import User
from rfid_library import SimpleMFRC522
from logging import info, debug


class Scanner(Thread):
    def __init__(self, device_id, database_manager: DatabaseManager):
        super().__init__()
        self.device_id = device_id
        self.database_manager = database_manager
        debug(f"Initializing scanner {self.device_id}")
        self.board = SimpleMFRC522(bus=0, device=device_id)
        debug(f"Scanner {self.device_id} initialized")
        self.mode = InteractionMode.NO_ACTION
        self.placement = Placement.ENTRANCE if device_id == 0 else Placement.EXIT
        self.is_modify_mode = False

    def run(self):
        info(f"Scanner {self.device_id} started")
        while True:
            tag_id = self.board.read()[0]
            info(tag_id)
            if self.mode == InteractionMode.READ:
                user = self.database_manager.get_user(tag_id)
                is_authorized = False if user is None else int(
                    user.is_authorized)
                if self.is_modify_mode:
                    self.handle_modify_user(user, tag_id)
                elif user is None or is_authorized == Authorization.UNAUTHORIZED.value:
                    self.handle_unauthorized_user(tag_id)
                elif is_authorized == Authorization.AUTHORIZED.value:
                    self.handle_authorized_user(tag_id)
                elif is_authorized == Authorization.ADMIN.value:
                    self.handle_admin_user()

                pass
            elif self.mode == InteractionMode.WRITE:
                pass

            sleep(2)

    def set_interaction_mode(self, mode: InteractionMode):
        self.mode = mode

    def handle_unauthorized_user(self, tag_id: int):
        info("Unauthorized!!")
        event = EventType.DENIED_ENTRANCE if self.isEntrance() else EventType.DENIED_LEAVE
        self.database_manager.create_log(tag_id, event)

    def handle_authorized_user(self, tag_id: int):
        # TODO open door
        info("Opening the door!!")
        event = EventType.AUTHORIZED_ENTRANCE if self.isEntrance() else EventType.AUTHORIZED_LEAVE
        self.database_manager.create_log(tag_id, event)

    def handle_admin_user(self):
        info("Kneel in front of the admin!!")
        print("\n")
        self.database_manager.print_users()
        print("\n")
        self.database_manager.print_logs()
        print("\n")
        self.is_modify_mode = True

    def handle_modify_user(self, user: User, tag_id: int):
        if(user is not None):
            info("Removing user rights!!")
            self.database_manager.create_or_update_user(
                tag_id, Authorization.UNAUTHORIZED)
        else:
            info("Adding user!!")
            self.database_manager.create_or_update_user(
                tag_id, Authorization.AUTHORIZED)

        self.is_modify_mode = False

    def isEntrance(self):
        return self.placement == Placement.ENTRANCE
