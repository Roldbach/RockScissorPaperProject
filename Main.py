import cv2
import numpy as np
import time
from keras.models import load_model

def loadLabel(path="./labels.txt"):
    '''
        Load labels for all classes into an ordered list

        By default, the file containing all labels is stored
    under the root directory

    input:
        path: String, the path to the file storing labels

    return:
        result: list, contains the corresponding labels for all classes
    '''
    result=[]
    with open(path, "r") as file:
        for line in file:
            content=line.strip("\n").split(" ")
            result.append(content[1])
    return result

def checkLabel(prediction, label):
    '''
        Return the label based on the prediction from the model

    input:
        prediction: list, contains probabilities for all classes
        label: list, contains the corresponding labels for all classes

    return:
        result: String, the label of the prediction
    '''
    result=np.where(prediction==np.amax(prediction, axis=1))
    return label[int(result[1])]

label=loadLabel()
model = load_model('keras_model.h5')
cap = cv2.VideoCapture(0)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

while True: 
    ret, frame = cap.read()
    resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
    image_np = np.array(resized_frame)
    normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
    data[0] = normalized_image
    prediction = model.predict(data)
    cv2.imshow('frame', frame)
    # Press q to close the window
    print(checkLabel(prediction, label))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
            
# After the loop release the cap object
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()