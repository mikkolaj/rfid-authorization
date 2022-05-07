import pickle
import socket
import struct

from client.communications.Message import Message


class NetworkHandler:
    def __init__(self, multicast_group: str, multicast_port: int):
        self.__initialize_multicast_socket(multicast_group, multicast_port)

    def __initialize_multicast_socket(self, multicast_group: str, multicast_port: int):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((multicast_group, multicast_port))
        mreq = struct.pack("=4sl", socket.inet_aton(multicast_group), socket.INADDR_ANY)

        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        self.socket = sock

    def receive_multicast_message(self):
        data = self.socket.recv(4096)
        return pickle.loads(data)

    def send_multicast_message(self, message: Message) -> None:
        data = pickle.dumps(message)
        self.socket.send(data)
