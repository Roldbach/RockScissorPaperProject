import cv2
import numpy as np
import time

from Configuration import dimension, labelPath, normalization, resultPath

def loadLabel(path=labelPath):
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

def get_prediction(camera, model, label, dimension=dimension, normalization=normalization):
    '''
        Return the prediction based on the screenshot
    
    input:
        camera: cv2.VideoCapture, could capture the user's movement
        model: keras.model, the model used for image classification
        label: list, contains the corresponding labels for all classes   
        dimension: 2-D tuple, the dimension of the resized image
        normalization: Boolean, true if the image requires normalization
    
    return:
        result: string, the label of the prediction
    '''
    data=getScreenshot(camera, dimension, normalization)
    prediction=model.predict(data)
    return checkLabel(prediction, label)

def getScreenshot(camera, dimension=dimension, normalization=normalization):
    '''
        Get an screenshot from the camera and return 
    the normalized image with given dimension

    input:
        camera: cv2.VideoCapture, could capture the user's movement
        dimension: tuple, the dimension of the resized image
        normalization: Boolean, true if the image requires normalization

    return:
        result: 4-D np.ndarray, the resized image which could be used for
                prediction directly

    '''
    _, frame=camera.read()
    resizedFrame=cv2.resize(frame, dimension, interpolation=cv2.INTER_AREA)

    if normalization:
        resizedFrame=normalizeImage(resizedFrame)
    
    return np.expand_dims(resizedFrame, axis=0)

def normalizeImage(image):
    '''
        Normalize the image so it stays within the -1~1 scale
    
    input:
        image: 3D np.ndarray, image with the shape (height, width, channel)

    return:
        result: 3D np.ndarray, the normalized image with the same shape 
    '''
    return (image.astype(np.float32)/127.0)-1

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

def analyseResult(path=resultPath):
    '''
        Load all results from the text file and
    return the answer with the highest freqeucny

    input:
        path: string, the path to the result text file
    
    return:
        result: string, the final prediction from the computer
    '''
    result=""
    max=-1
    total={}
    try:
        with open(path,"r") as file:
            for line in file:
                content=line.strip("\n")
                if content not in total:
                    total[content]=1
                else:
                    total[content]+=1

        for key, value in total.items():
            if value>max:
                result=key
                max=value
        
        return result
    except:
        print("Can't load the result file. Please try again.")

def estimateTime(camera, model, label, dimension=dimension, normalization=normalization, number=1000):
    '''
        Estimate the runtime for the function get_prediction() by
    calculating the average time for running given number of times

        The average time for 1 running is: 0.06122515368461609s when
    running 1000 times but 0.906531572341919s when running 1 time on
    my own laptop

    input:
        camera: cv2.VideoCapture, could capture the user's movement
        model: keras.model, the model used for image classification
        label: list, contains the corresponding labels for all classes   
        dimension: 2-D tuple, the dimension of the resized image
        normalization: Boolean, true if the image requires normalization
        number: int, the total number of times to run the get_prediction()
    
    return:
        result: float, the average time to run the function for 1 time
    '''
    start=time.time()
    for i in range(number):
        get_prediction(camera, model, label, dimension, normalization)
    end=time.time()
    return (end-start)/number


