import time

from camera_rps import get_prediction
from Configuration import dimension, limit, normalization, rate, resultPath
from threading import Thread

class PredictionThread(Thread):
    def __init__(self, camera, model, label, dimension=dimension, normalization=normalization, number=limit*rate, path=resultPath):
        '''
            This class contains the following attributes:
            (1) camera: cv2.VideoCapture, could capture the user's movement
            (2) model: keras.model, the model used for image classification
            (3) label: list, contains the corresponding labels for all classes   
            (4) dimension: 2-D tuple, the dimension of the resized image
            (5) normalization: Boolean, true if the image requires normalization
            (6) number: int, the total number of times to capture screenshots
            (7) path: string, the path to save results
        '''
        Thread.__init__(self)
        self.camera=camera
        self.model=model
        self.label=label
        self.dimension=dimension
        self.normalization=normalization
        self.number=number
        self.path=path
    
    def run(self):
        '''
            Capture a number of scrrenshots and store the corresponding
        labels into the result text file

            The more the scrrenshots are captured, the more accurate the final
        prediction would be
        '''
        with open(self.path,"w") as file:
            for i in range(self.number):
                file.write(get_prediction(self.camera, self.model, self.label, self.dimension, self.normalization)+"\n")

class CountDownThread(Thread):
    def __init__(self, limit=limit):
        '''
            This class contains the following attribute:
            (1) limit: int, the time to count down, unit: second
        '''
        Thread.__init__(self)
        self.limit=limit

    def run(self):
        '''
            Display the count down to the user
        '''
        for i in range(self.limit, 0, -1):
            print(f"Please wait for {i} s!")
            time.sleep(1)

