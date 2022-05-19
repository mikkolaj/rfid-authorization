from logging import info, debug
from threading import Thread

from client.interaction.Door import Door
from client.interaction.InteractionMode import InteractionMode
from client.interaction.Scanner import Scanner
from client.networking.Host import Host
from client.persistance.DatabaseManager import DatabaseManager


class InteractionManager(Thread):
    def __init__(self, host: Host, database_manager: DatabaseManager):
        super().__init__()
        debug("Starting InteractionManager")
        self.door = Door()
        self.door.start()
        info("Door thread started")

        self.scanner_1 = Scanner(0, host, self.door, database_manager)
        self.scanner_2 = Scanner(1, host, self.door, database_manager)

        self.scanner_1.start()
        info("Scanner 1 thread started")
        self.scanner_2.start()
        info("Scanner 2 thread started")

    def run(self) -> None:
        self.scanner_1.set_interaction_mode(InteractionMode.READ)
        self.scanner_2.set_interaction_mode(InteractionMode.READ)
