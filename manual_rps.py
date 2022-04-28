import cv2
import numpy as np
import random
import time

from keras.models import load_model

def play():
    '''
        Play the RPS game with a NPC who randomly choose
    from available options
    '''
    user=get_user_choice()
    computer=get_computer_choice()
    winner=get_winner(computer, user)
    print(winner)

#To Finish
def playWithAI():
    '''

    '''
    return

def get_computer_choice(option=["scissors", "rock", "paper"]):
    '''
        Randomly pick an option from available choices
    and return it

    input:
        option: list, contains all options the computer
                could choose from
    
    return:
        result: String, the final choice from the computer
    '''
    return option[random.randrange(0, len(option))]

def get_user_choice(content="Please choose from scissors, rock, and paper: ", option={"scissors", "rock", "paper"}):
    '''
        Ask the user to enter the choice until a valid
    input is obtained

        Both uppercase and lowercase are allowed

        White spaces are automatically omitted and don't
    contribute to the result

        If the user enters a invalid input, he would be
    asked to re-enter a new one after 1s
    
    input:
        content: String, the content displayed to the user when asking for an input
        option: list, contains all results considered as valid inputs

    return:
        result: String, the final result from the user
    '''
    while True:
        result=input(content)
        if result.strip(" ").lower() in option:
            return result.strip(" ").lower()
        else:
            print("Not a valid input. Please try again.\n")
            time.sleep(1)

def get_winner(computer, user):
    '''
        Return the winner of the game (either the computer or the user)
    based on the rule

        If both the computer and the user choose the same option,
    the game is a draw

    input:
        computer: String, the choise from the computer
        user: String, the choice from the user
    
    return:
        result: String, speciifies the winner of the game or draw
    '''
    winCondition={("paper","rock"), ("rock","scissors"), ("scissors","paper")}
    if computer==user:
        return "The game is a draw."
    elif (computer,user) in winCondition:
        return "The winner is NPC!"
    else:
        return "The winner is you!"

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

def getScreenshot(camera, dimension=(224,224), normalization=True):
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

label=loadLabel()
model=load_model('keras_model.h5')
camera=cv2.VideoCapture(0)

while True: 
    data=getScreenshot(camera)
    prediction = model.predict(data)
    #cv2.imshow('frame', frame)
    # Press q to close the window
    print(checkLabel(prediction, label))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break      
# After the loop release the cap object
camera.release()
# Destroy all the windows
cv2.destroyAllWindows()