import cv2
import os
import time

from camera_rps import analyseResult, loadLabel
from Configuration import correctContent, dimension, introduction, labelPath, level, levelContent, limit, loseContent, modelPath, normalization, option, optionContent, rate, resultPath, winContent
from keras.models import load_model
from manual_rps import get_computer_choice, get_user_choice, get_winner
from NewThread import CountDownThread, PredictionThread

class NPC:
    '''
        The class that could guide the user to play the RPS game
    '''
    def __init__(self, introduction=introduction, level=level, option=option,
                levelContent=levelContent, optionContent=optionContent, correctContent=correctContent, winContent=winContent, loseContent=loseContent,
                modelPath=modelPath, labelPath=labelPath, resultPath=resultPath, dimension=dimension, normalization=normalization,
                limit=limit, rate=rate):
        '''
            This class contains the following attributes:
            (1) introduction: list, welcome the user and explain basic rules
            (2) level: set, contains all options considered as valid game levels
            (3) option: list, contains all results considered as valid options
            (4) levelContent: string, the content displayed to the user when asking for the level
            (5) optionContent: string, the content displayed to the user when asking for the option
            (6) correctContent: list, the content displayed to the user when asking whether the 
                                prediction was correct or not
            (7) winContent: string, the content displayed to the user when winning the game
            (8) loseContent: string, the content displayed to the user when losing the game
            (9) resultPath: string, the path to save results
            (10) dimension: 2-D tuple, the dimension of the resized image
            (11) normalization: Boolean, true if the image requires normalization
            (12) limit: int, the time to countdown, unit: second
            (13) rate: int, the number of screenshots captured per second    
            (14) score: dictionary, records the scores for the user and the NPC
            (15) round: int, the number of rounds that has been played so far
            (16) correct: int, the number of rounds that the prediction is right verified by the user
            (17) camera: cv2.VideoCapture, could capture the user's movement
            (18) model: keras.model, the model used for image classification
            (19) label: list, contains the corresponding labels for all classes

        '''
        self.introduction=introduction
        self.level=level
        self.option=option
        self.levelContent=levelContent
        self.optionContent=optionContent
        self.correctContent=correctContent
        self.winContent=winContent
        self.loseContent=loseContent
        self.resultPath=resultPath
        self.dimension=dimension
        self.normalization=normalization
        self.limit=limit
        self.rate=rate

        self.score={"NPC":0, "user":0}
        self.round=0
        self.correct=0
        self.camera=cv2.VideoCapture(0)
        self.model=load_model(modelPath)
        self.label=loadLabel(labelPath)

        result=self.welcome()
        if result=="quit":
            self.quit()
        elif result=="easy":
            self.easyStart()
        else:
            self.hellStart()
        
    def welcome(self):
        '''
            Display the welcome information, basic rules to
        the user and ask the user for the level of game

        return:
            result: string, the game level obtained from the user
        '''
        os.system("cls||clear")
        for line in introduction:
            print(line)
        
        return get_user_choice(self.levelContent, self.level)
    
    def easyStart(self):
        '''
            Start the game with easy level by following steps:
            (1) Display the current round number
            (2) Ask the user for a valid input from scissors,
                rock and paper
            (3) Randomly generate an option
            (4) Compare those results and determine the winner
                of this round
            (5) Leave some time for the user to read the result
            (6) Check whether the game is over, display the final
                winner if it is

            Within this mode, the NPC will randomly choose
        from all available options

            There is no upper limit to the round considering everytime
        both choose the same option
        '''
        while True:
            self.displayRound()
            userResult=get_user_choice(self.optionContent, set(self.option))
            NPCResult=get_computer_choice(self.option)
            
            winner=get_winner(NPCResult, userResult)
            self.addScore(winner)

            self.displayWinner(winner)
            self.displayScore()
            time.sleep(2)

            if self.checkStatus():
                self.displayFinal()
                self.quit()
                return
    
    def hellStart(self):
        '''
            Start the game with hell level by following steps:
            (1) Display the current round number
            (2) Display countdown to the user while generating prediction
            (3) Response to the final prediction
            (4) Compare those results and determine the winner of this round
            (5) Ask the user whether this prediction is correct or not
            (6) Check whether the game is over, display the final
                winner if it is
        '''
        while True:
            self.displayRound()
            time.sleep(3)
            userResult, NPCResult=self.countDown()
            
            winner=get_winner(NPCResult, userResult)
            self.addScore(winner)

            self.displayWinner(winner)
            self.displayScore()
            self.displayOption(userResult, NPCResult)
            self.askCorrect()

            if self.checkStatus():
                self.displayFinal()
                print(f"The accuracy of prediction of the whole game is: {100*self.correct/self.round}%")
                self.quit()
                return
                
    def displayRound(self):
        '''
            Clear the terminal output and display the current
        round number

            Everytime this function is called, the round number
        is increased by 1
        '''
        self.round+=1
        os.system("cls||clear")
        print(f"---------- Round {self.round} ----------")

    def countDown(self):
        '''
            Capture screenshots and analyse those to get the final
        result while displaying the countdown to the user, finally
        return the prediction and the corresponding response from NPC

        return:
            userResult: string, the user's option based on screenshots
            NPCResult: string, the corresponding option based userResult
        '''
        predictionThread=PredictionThread(self.camera, self.model, self.label, self.dimension, self.normalization, self.limit*self.rate, self.resultPath)
        countDownThread=CountDownThread(self.limit)
        
        predictionThread.start()
        countDownThread.start()
        predictionThread.join()
        countDownThread.join()

        userResult=analyseResult(self.resultPath)
        NPCResult=self.chooseOption(userResult)

        return userResult, NPCResult

    def chooseOption(self, prediction):
        '''
            Within the hell mode, the NPC could choose based on the
        prediction to make sure the user loses this round (if the 
        prediction is accurate) or the game is draw (if nothing is detected)

        return:
            result: the option to win the game based on the prediction
        '''
        if prediction=="scissors":
            return "rock"
        elif prediction=="rock":
            return "paper"
        elif prediction=="paper":
            return "scissors"
        else:
            return "nothing"

    def addScore(self, winner):
        '''
            Change the score according to the winner
        information provided by the function get_winner()

        input:
            winner: string, the winner information displayed
                    to the user
        '''
        if "draw" in winner:
            return
        elif "NPC" in winner:
            self.score["NPC"]+=1
        else:
            self.score["user"]+=1

    def displayWinner(self, winner):
        '''
            Display the winner of the round to the user
        '''
        print(" ")
        print(winner)

    def displayScore(self):
        '''
            Display the current score to the user
        '''
        print(" ")
        print("Your score is:", self.score["user"])
        print("Your component's score is:", self.score["NPC"])

    def displayOption(self, userResult, NPCResult):
        '''
            Display the prediciton and the response within
        a certain round
        '''
        print(" ")
        print("Within this round your option is: "+userResult)
        print("Within this round your component's option is: "+NPCResult)

    def askCorrect(self):
        '''
            Ask whether the prediction within this round is
        correct or not
        '''
        print(" ")
        for i in range(len(self.correctContent)-1):
            print(self.correctContent[i])
        
        result=get_user_choice(self.correctContent[-1], {"yes","no"})
        
        if result=="yes":
            self.correct+=1
        
    def checkStatus(self):
        '''
            Determine whether to stop the game by check whether
        one has reached the 3 wins
        
        return:
            result: boolean, true if the game is over
        '''
        for value in self.score.values():
            if value==3:
                return True
        return False

    def displayFinal(self):
        '''
            Display the final winner according to
        the score
        '''
        for key, value in self.score.items():
            if value==3:
                winner=key
        
        os.system("cls||clear")
        if winner=="user":
            print(self.winContent)
        else:
            print(self.loseContent)
    
    def quit(self):
        '''
            Release the camera before quiting the game
        '''
        self.camera.release()
        
