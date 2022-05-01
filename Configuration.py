#The welcome and the introduction to the user
introduction=[
    "Welcome to the Rock, Paper, Scissors game made by roldbach.",
    " ",
    "Which level of the game would you like to try?",
    "a. Easy: your component will randomly pick the option.",
    "b. Hell: you will feel the power.",
    " ",
    "To feel the real power in the hell level, Please position yourself in the first 3 sconds and hold that during the countdown.",
    " "
]

#Available options that the computer could choose
option=["scissors", "rock", "paper"]

#The path to the label text file
labelPath="./labels.txt"

#The level of the game
level={"easy", "hell", "quit"}

#The time limit to countdown, unit: second
limit=5

#The path to the model h5 file
modelPath="./keras_model.h5"

#The number of times to get prediction per second
rate=10

#The path to the result text file
resultPath="./result.txt"

#The dimension to resize the image
dimension=(224,224)

#Whether to normalize the image
normalization=True

#The content to display to the user when asking for an input
optionContent="Please choose from scissors, rock, and paper: "

#The content to display to the user when asking for the level of the game
levelContent="Please choose from easy, hell and quit: "

#The content to display to the user when winning the game
winContent="Congratulations! You have won the game! Good job!"

#The content to display to the user when losing the game
loseContent="You have lost the game. Good luck next time."

#The content to display to the user when asking whether the prediction is correct
correctContent=["Did your component get the correct prediction?","Please choose from yes or no: "]

