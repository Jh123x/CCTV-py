import socket
import pickle
import multiprocessing as mp
import cv2

class Server:
    def __init__(self, ip:str, port:int):
        """Server object to receive the frames sent over"""
        self.addr = (ip, port)
        self.mutex = mp.Semaphore(1)
        self.count = 0

    def get_addr(self):
        return self.addr

    def bind(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(self.addr)

    def process(self, soc):
        """Process the socket"""
        #Thread safe count increment
        self.mutex.acquire(True)
        count = self.count
        self.count += 1
        self.mutex.release()

        #Create a video writer
        vid_writer = cv2.VideoWriter(f'output{count}.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640,480))
        while soc.connect_ex(self.addr) == 0:
            data = pickle.loads(soc.recv(2048))
            vid_writer.write(data)

        #Close the vidwrite
        vid_writer.release()

    def mainloop(self):
        """Start serving the client"""

        #Start listening for incoming connections
        self.socket.listen(5)
        print("Server is ready to receive")

        #While loop to listen to connections
        while True:
            soc, addr = self.socket.accept()
            self.process(soc)
            

