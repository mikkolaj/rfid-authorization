class PeerCommunicationManager:
    def __init__(self):
        self.is_king = False

    def find_peers(self):
        pass

    def send_im_alive(self):
        pass

    def initialize(self):
        pass

    def check_if_king(self):
        pass

    def run(self):
        self.initialize()

        while True:
            message = self.receive_message()

