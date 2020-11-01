import cv2
from multiprocessing import Queue, Process

class Camera:
    def __init__(self, queue, src:int = 0):
        """Creates the camera object"""

        #Stores the source of the camera
        self.src = src

        #Store the queue to store the frames
        self.queue = queue

        #Status
        self.set_status(True)

    def get_status(self):
        """Get the status of the camera"""
        return self.status

    def get_queue(self):
        """Get the queue used to store the frames"""
        return self.queue

    def set_status(self, status:bool):
        """Set the status of the camera"""
        self.status = status

    def mainloop(self):
        """The mainloop to poll for the frames on the camera"""

        #Capture object
        self.cap = cv2.VideoCapture(self.src)
        
        while (self.status):
            # Capture frame-by-frame
            ret, frame = self.cap.read()
            self.queue.put(frame)
    
def show(queue: Queue) -> None:
    """Show the screen for the CCTV"""
    #Infinite loop
    while True:

        #Get the frame from the queue
        frame = queue.get()

        # Display the resulting frame
        cv2.imshow('frame', frame)

        #Press q to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    #Clear all windows after the process is over
    cv2.destroyAllWindows()


def run_camera(queue, src:int) -> None:
    """Run the camera and poll frames into the queue"""
    #Create a camera
    cam = Camera(queue, src)

    #Run the mainloop to poll
    cam.mainloop()

def initialise() -> Queue: 
    #Create a process safequeue
    queue = Queue()
    return queue

def start_poll(src:int, queue:Queue, daemon:bool = True) -> None:
    """Start the polling of the camera"""
    #Create a thread to poll from the camera
    process = Process(target = run_camera, args = (queue, src))

    #Set the program to quit if the mainthread exits
    process.daemon = daemon

    #Start the process
    process.start()

def main() -> None:
    """Main function"""
    queue = initialise()

    #Set the source
    src = 0

    #Start polling the camera
    start_poll(src, queue, True)

    #Show the results of the queue
    show(queue)
    
#Main function for python
if __name__ == "__main__":
    main()