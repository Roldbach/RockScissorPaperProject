import cv2
import os
import time

from camera_rps import loadLabel
from Configuration import dimension, introduction, labelPath, level, levelContent, limit, modelPath, normalization, rate, resultPath
from keras.models import load_model
from manual_rps import get_user_choice
from NewThread import CountDownThread, PredictionThread

class NPC:
    '''
        The class that could guide the user to play the RPS game

        The process of a whole game is shown as below:
        (1) Welcome the user and display the basic rules
        (2) If the user choose to start the game, play the game
            a. Ask the user for input
            b. Display the count down and analyse the result
            c. Response to the prediction according to the game level
        (3) If certain rules is met, the game will finish and the final
            winner will be displayed
    '''
    def __init__(self, introduction=introduction, level=level, modelPath=modelPath, labelPath=labelPath, 
                dimension=dimension, normalization=normalization, limit=limit, rate=rate, resultPath=resultPath):
        '''
            This class contains the following attributes:
            (1) introduction: list, welcome the user and explain basic rules
            (2) level: set, contains all options considered as valid game levels
            (3) levelContent: string, the content displayed to the user when asking for the level
            (2) score: dictionary, records the scores for the user and the computer
            (3) round: int, the number of rounds that has been played so far
            (4) correct: int, the number of rounds that the prediction is right verified by the user
            (4) camera: cv2.VideoCapture, could capture the user's movement
            (5) model: keras.model, the model used for image classification
            (6) label: list, contains the corresponding labels for all classes   
            (7) predictionThread: PredictionThread, the class to handle the prediction thread
            (8) countDownThread: CountDownThread, the class to handle the count down

        '''
        self.introduction=introduction
        self.level=level
        self.levelContent=levelContent
        self.score={"computer":0, "user":0}
        self.round=0
        self.correct=0

        self.camera=cv2.VideoCapture(0)
        self.model=load_model(modelPath)
        self.label=loadLabel(labelPath)

        self.predictionThread=PredictionThread(self.camera, self.model, self.label, dimension, normalization, limit*rate, resultPath)
        self.countDownThread=CountDownThread(limit)

        result=self.welcome()

    def welcome(self):
        '''
            Display the welcome information, basic rules to the user
        and ask the user for the level of game

        return:
            result: string, the game level obtained from the user
        '''
        os.system("cls||clear")
        for line in introduction:
            print(line)
        
        return get_user_choice(self.levelContent, self.level)
        
