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
        self.closed = False

    def get_addr(self):
        """Get the address, port"""
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
        while not self.closed:
            data = packet = soc.recv(4096)
            if data:
                self.closed = True
            data = pickle.loads(data)
            vid_writer.write(data)

        #Decrement count
        self.mutex.acquire(True)
        self.count -= 1
        self.mutex.release()

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
            

if __name__ == "__main__":
    server = Server("localhost", 1234)
    server.bind()
    server.mainloop()