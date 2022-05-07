import pickle
import socket
import struct

from client.networking.NetworkConfig import MULTICAST_PORT, MULTICAST_GROUP
from client.networking.messages.Message import Message


class NetworkHandler:
    def __init__(self):
        self.__initialize_multicast_socket(MULTICAST_GROUP, MULTICAST_PORT)

    def __initialize_multicast_socket(self, multicast_group: str, multicast_port: int) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((multicast_group, multicast_port))
        mreq = struct.pack("=4sl", socket.inet_aton(multicast_group), socket.INADDR_ANY)

        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        self.socket = sock

    def receive_multicast_message(self) -> Message:
        data, address = self.socket.recvfrom(4096)
        message: Message = pickle.loads(data)
        message.sender = address

        return message

    def send_multicast_message(self, message: Message) -> None:
        data = pickle.dumps(message)
        self.socket.send(data)

    def send_unicast_message(self, message: Message, address: str) -> None:
        data = pickle.dumps(message)
        self.socket.sendto(data, address)
