from client.communications.MessageType import MessageType


class Message:
    def __init__(self, message_type: MessageType):
        self.message_type = message_type


