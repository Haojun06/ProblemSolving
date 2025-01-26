import time
import threading
import random
import json
import os


user_answer = None

def get_input():
    #modify the user_answer into global
    global user_answer
    user_answer = input()

def gen_qtn(level):
    #every level have diffrent question
    if level == 'Easy':
        #randomly pick from 1 to 10 for num1 and num2
        #random.randint needed within a spesific range
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        #randomly pick from the list
        #random.choice return a randomly selected element from a sequence
        opt = random.choice(['+', '-', '*'])

    elif level == 'Hard':
        num1 = random.randint(1, 15)
        num2 = random.randint(1, 15)
        opt = random.choice(['+', '-', '*','/'])

    elif level == 'Extreme':
        num1 = random.randint(1, 30)
        num2 = random.randint(1, 30)
        opt = random.choice(['+', '-', '*','/','**','%'])

    #check wheter the denominator is 0
    if opt=="/" and num2==0:
        #if yes pick the num2 again
        num2=random.randint(1,10)

    #using the num1 num2 opt provided generate a question
    question = (f"{num1}{opt}{num2}")
    #calculate the answer of the question
    answer = eval(question)
    return question, answer

def time_per_question(answer, time_limit):
    global user_answer
    user_answer = None

    #create a thread to run the get input function
    input_thread = threading.Thread(target=get_input)
    #start the thread
    input_thread.start()

    #function will continue after the time limit end without bothering the input thread completed or not
    input_thread.join(timeout=time_limit)

    #if user didnt input anything within the time limit the function will print time out and the correct answer
    if user_answer == None:
        print("\nTime Out")
        print(f"The correct answer is {answer}")
        #return false to the main function
        return False

    if user_answer.lower() == "quit":
        print("You quit the quiz")
        #return quit to the main funtion
        return 'quit'
    #try wheter the user_answer is valid input(numeric)
    try:
        if float(user_answer) == answer:
            print("You're correct")
            #return true to the main function
            return True
        else:
            print(f"The correct answer is {answer}")
            #return false to the main function
            return False
        
    except ValueError:
        print("Invalid Input")
        #print invalid input and skip to the next question

def math_quiz():
    time_limit = [10, 8, 6]
    num_questions = 5
    question_correct=0
    score = 0
    levels = ["Easy", "Hard", "Extreme"]
    cont_game = 'yes'
    mark=[1,2,3]

    #Instruction for math quiz
    print("Welcome to Math Quiz")
    #wait for 1 second for readability
    time.sleep(1)
    print("Nice to meet you")
    time.sleep(1)
    print("You will score diffrent mark for every level")
    print("You will score 1 mark for each question in Easy level which is level 1")
    print("You will score 2 mark for each question in Hard level which is level 2")
    print("You will score 3 mark for each question in Extreme level which is level 3")
    time.sleep(2)
    print("(Enter 'quit' to exit the quiz at any time)")


    level_index = 0  # Start from the first level
    #while loop will continue until the level index is more than the len of levels which is 3
    while level_index < len(levels):
        #select the level from the levels list
        level = levels[level_index]
        print(f"Starting Level {level_index + 1}: {level}")
        i = 1  # Initialize the counter for questions

        while i <= num_questions:
            #wait for 1 second for readability
            time.sleep(1)
            #print the number of question
            print(f"Question {i}/{num_questions}:")
            #call the gen_qtn function and give the level to the function
            #function generate the question based on the level
            #gen_qtn function return a tuple with two elements
            #question,answer= gen_qtn(level) is unpacking the tuple into two elements
            question, answer = gen_qtn(level)
            #print the time limit for each question and the question
            print(f"Time limit: {time_limit[level_index]}seconds\nWhat is your answer for {question}")
            #call the tim_per_question function with the info answer and the time limit
            #unpack the result to a element
            result = time_per_question(answer, time_limit[level_index])
            #if user input is quit
            if result == 'quit':
                #it shows that the user dont want to continue the game
                cont_game = "no"
            #quit from the loop
                break

            #if user answer is correct
            if result==True:
                #the question will add 1
                question_correct=question_correct+1
                #the score will be scored based on the level the user are playing
                score =score+ mark[level_index]

            i += 1  # Increment the question counter

        #if the user dont want to continue the game
        if cont_game == 'no':
            #user quit from the loop
            break

        
        #print the question user have successfully answered and the score the user scored
        print(f"You successfully answered {question_correct} questions correctly and your score is {score}")
        
        #if the game havent finish
        if level_index<2:
            #in the end of every level the user will be asked wheter the user want to continue or not
            cont_game = input("Do you want to continue the game? (yes/no): ").lower()
            #if the user dont want to continue 
            if cont_game == "no":
            #quit from the loop
                break
        #if the user have arrive the end of the extreme level
        else:
            #automatically quit the loop
            break
        
        level_index += 1  # Move to the next level

    #save the score in the leaderboard
    leaderboard=f"Math quiz score:{score}"

    #check the file is exist or not
    #if yes
    if os.path.exists("data.json"):
        #open the file
        with open("data.json", "r") as file:
            data = json.load(file)  # Load existing data

    #if no
    else:
        #open a new file
        data = []

    #add the leaderboard into the data
    data.append(leaderboard)
        
#checks if the script is being executed directly
if __name__ == "__main__":
    math_quiz()
