import time
import os
import cv2

from keras.models import load_model
from NewThread import PredictionThread, CountDownThread
from camera_rps import loadLabel
from Configuration import modelPath

label=loadLabel()
model=load_model(modelPath)
camera=cv2.VideoCapture(0)

t1=PredictionThread(camera, model, label, number=50)
t2=CountDownThread()
start=time.time()
t1.start()
t2.start()
t1.join()
t2.join()
end=time.time()
print(f"The final time is: {end-start}")

# After the loop release the cap object
camera.release()
# Destroy all the windows
cv2.destroyAllWindows()