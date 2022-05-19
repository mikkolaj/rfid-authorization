from logging import info, debug
from threading import Thread

from client.interaction.BoardButton import BoardButton
from client.interaction.InteractionMode import InteractionMode
from client.interaction.Scanner import Scanner
from client.persistance.DatabaseManager import DatabaseManager


class InteractionManager(Thread):
    def __init__(self, database_manager: DatabaseManager):
        super().__init__()
        debug("Starting InteractionManager")
        self.scanner_1 = Scanner(0, database_manager)
        self.scanner_2 = Scanner(1, database_manager)

        self.scanner_1.start()
        info("Scanner 1 thread started")
        self.scanner_2.start()
        info("Scanner 2 thread started")

        self.button = BoardButton()
        self.button.start()
        info("Board button thread started")

    def run(self) -> None:
        self.scanner_1.set_interaction_mode(InteractionMode.READ)
        self.scanner_2.set_interaction_mode(InteractionMode.READ)
