import random
import time

from Configuration import option, content

def play():
    '''
        Play the RPS game with a NPC who randomly choose
    from available options
    '''
    user=get_user_choice()
    computer=get_computer_choice()
    winner=get_winner(computer, user)
    print(winner)

def get_computer_choice(option=option):
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

def get_user_choice(content=content, option=set(option)):
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
        option: set, contains all results considered as valid inputs

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