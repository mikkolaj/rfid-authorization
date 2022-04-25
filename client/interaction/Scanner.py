from threading import Thread

from client.interaction.InteractionMode import InteractionMode
from rfid_library import SimpleMFRC522
from logging import info, debug


class Scanner(Thread):
    def __init__(self, device_id):
        super().__init__()
        self.device_id = device_id
        debug(f"Initializing scanner {self.device_id}")
        self.board = SimpleMFRC522(bus=0, device=device_id)
        debug(f"Scanner {self.device_id} initialized")
        self.mode = InteractionMode.NO_ACTION

    def run(self):
        info(f"Scanner {self.device_id} started")
        while True:
            id, text = self.board.read()
            info(id)
            info(text)
            info(self.mode)
            if self.mode == InteractionMode.READ:
                pass
            elif self.mode == InteractionMode.WRITE:
                pass

    def set_interaction_mode(self, mode: InteractionMode):
        self.mode = mode
