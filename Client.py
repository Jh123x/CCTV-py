import socket
import pickle

class CCTVClient:
    def __init__(self, ip:str, port:int):
        """Create a client object to send the frames"""
        self.addr = (ip, port)

    def get_addr(self) -> tuple:
        """Get the (ip,port) of the server"""
        return self.addr

    def connect(self):
        """Connect to the server"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, obj) -> None:
        """Send an object to the server"""
        self.socket.send(pickle.dumps(obj))

    def close(self):
        self.socket.close()