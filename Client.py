import socket
import pickle
import cv2
import camera

class CCTVClient:
    def __init__(self, ip:str, port:int):
        """Create a client object to send the frames"""
        self.addr = (ip, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def get_addr(self) -> tuple:
        """Get the (ip,port) of the server"""
        return self.addr

    def connect(self):
        """Connect to the server"""
        self.socket.connect(self.get_addr())

    def send(self, obj) -> None:
        """Send an object to the server"""
        self.socket.send(pickle.dumps(obj))

    def close(self):
        self.socket.close()

def main():
    """Main function of the client"""

    #Create a CCTV client
    client = CCTVClient("localhost", 1234)

    #Initialise the queue
    queue = camera.initialise()

    #Start polling
    camera.start_poll(0, queue)

    client.connect()
    while True:
        image = queue.get()
        retval, buffer = cv2.imencode('.jpg', image)
        client.send(buffer)

    client.close()
        

if __name__ == "__main__":
    main()