#The welcome and the introduction to the user
introduction=[
    "Welcome to the Rock, Paper, Scissors game made by roldbach.",
    " ",
    "Which level of the game would you like to try?",
    "a. Easy: your component will randomly pick the option.",
    "b. Hell: you will feel the power.",
    " "
]

#Available options that the computer could choose
option=["scissors", "rock", "paper"]

#The path to the label text file
labelPath="./labels.txt"

#The level of the game
level={"easy", "hell", "quit"}

#The time limit to count down, unit: second
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
content="Please choose from scissors, rock, and paper: "

#The content to display to the user when asking for the level of the game
levelContent="Please choose from easy, hell and quit: "