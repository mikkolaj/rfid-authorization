from threading import Thread
from threading import Timer

from client.communications.NetworkConfig import ROOT_TIMEOUT_SECONDS
from client.communications.NetworkHandler import NetworkHandler



class Host(Thread):
    def __init__(self):
        super().__init__()
        self.root = None
        self.network_handler = NetworkHandler()
        self.best_mac = None
        self.mac = None

    def run(self):
        self.connect()

    def connect(self):
        interpreter = Thread(target=self.interpret_messages)
        r = Timer(ROOT_TIMEOUT_SECONDS, self.set_root)
        """
        sł
        """

    def interpret_messages(self):
        self.networkHandler.receive_multicast_message()

    def compare_mac(self):
        pass

    def set_root(self):
        self.compare_mac(self.best_mac, self.mac)
#         I COS TAM SE DALEJ
