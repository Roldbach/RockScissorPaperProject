# RockScissorPaperProject

## MileStone 1
- I have created a simple model that could do image classification tasks and download them with labels.
- This model could have 4 different outcomes: Rock, Scissor, Paper and Nothing. The model could capture significant features within the input image and use that to determine the corresponding categoriy of the image. Finally, the class with the highest probability is the output.
- To maximize the model accuracy, I used a very big "feature" which could entirely block my face when Scissor, Rock, Paper options were chosen. In this way, the model could easily distinguish between different classes by checking the presence of my face as well as the shape of my hand. The drawback of this method is that the model couldn't generalize well and will fail to accurately predict under other situations.
- The hyperparameters were set by experience where generally a 100 epoch would work for such a easy task. The batch size was chosen to be 256 and the learning rate was chosen to be 0.001. Hopefully it was trained by Adam.
- Before downloading the model, several simple tests were done, which showed that the model was not that accurate as it couldn't output one high probability while the other 3 probabilities stay low, indicating that the model is unsure.
- The model was downloaded and could be further used easily. 
![Model Training](Image/ModelTraining.png)

## MileStone 2
- I have constructed a function that could randomly generate a choice from all available options and ask the user to enter a valid input. Finally, those results could be used to determine who is the winner according to the rule of the game.
- To randomly generate a result from all available options, I simply generate a random index which is within the range from 0 to the length of the list containing all options, which is shown as below:
```python
    def get_computer_choice(option=["scissors", "rock", "paper"]):
        return option[random.randrange(0, len(option))]
```
- The input entered by the user is checked everytime to make sure the game could run smoothly later. If the input is invalid, the user would be asked for entering another one again after 1 second until one valid option is entered, which is shown as below:
```python
    def get_user_choice(content="Please choose from scissors, rock, and paper: ", option={"scissors", "rock", "paper"}):
        while True:
            result=input(content)
            if result.strip(" ").lower() in option:
                return result.strip(" ").lower()
            else:
                print("Not a valid input. Please try again.\n")
                time.sleep(1)
```
- In order to determine the winner of the game or whether it is a draw, results from both computer and the user are compared. I simply listed the conditions when the winner is NPC and when it is a draw, otherwise the winner would be the user. The core function is shown below:
```python
    def get_winner(computer, user):
        winCondition={("paper","rock"), ("rock","scissors"), ("scissors","paper")}
        if computer==user:
            return "The game is a draw."
        elif (computer,user) in winCondition:
            return "The winner is NPC!"
        else:
            return "The winner is you!"
```
- The play() function is just simply combining everything together and making the game running smoothly, which could be found as below:
```python
    def play():
        user=get_user_choice()
        computer=get_computer_choice()
        winner=get_winner(computer, user)
        print(winner)
```
- I used lots of default arguments when defining a function so the user doesn't have to code a lot.
