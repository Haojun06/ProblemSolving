import time
import threading
import random
import json
import os


user_answer = None

def get_input():
    global user_answer
    user_answer = input()

def gen_qtn(level):
    if level == 'Easy':
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        opt = random.choice(['+', '-', '*'])
    elif level == 'Hard':
        num1 = random.randint(1, 15)
        num2 = random.randint(1, 15)
        opt = random.choice(['+', '-', '*','/'])
    elif level == 'Extreme':
        num1 = random.randint(1, 30)
        num2 = random.randint(1, 30)
        opt = random.choice(['+', '-', '*','/','**','%'])

        if opt=='/':
            num2= random.randint(1,5)

        if opt=='**':
            num2= random.randint(1,3)

    question = (f"{num1}{opt}{num2}")
    answer = eval(question)
    return question, answer

def time_per_question(answer, time_limit):
    global user_answer
    user_answer = None

    input_thread = threading.Thread(target=get_input)
    input_thread.start()

    input_thread.join(timeout=time_limit)

    if user_answer == None:
        print("\nTime Out")
        print(f"The correct answer is {answer}")
        return False

    if user_answer.lower() == "quit":
        print("You quit the quiz")
        
        return 'quit'
    try:
        if float(user_answer) == answer:
            print("You're correct")
            return True
        else:
            print(f"The correct answer is {answer}")
            return False
    except ValueError:
        print("Invalid Input")

def math_quiz():
    time_limit = [10, 8, 6]
    num_questions = 3
    question_correct=0
    score = 0
    levels = ["Easy", "Hard", "Extreme"]
    cont_game = 'yes'
    mark=[1,2,3]

    print("Welcome to Math Quiz")
    time.sleep(1)
    print("Nice to meet you")
    time.sleep(2)
    print("You will score diffrent mark for every level")
    print("You will score 1 mark for each question in Easy level which is level 1")
    print("You will score 2 mark for each question in Hard level which is level 2")
    print("You will score 3 mark for each question in Extreme level which is level 3")
    time.sleep(1)
    print("You can quit the quiz anytime with just enter quit")


    level_index = 0  # Start from the first level
    while level_index < len(levels):
        level = levels[level_index]
        print(f"Starting Level {level_index + 1}: {level}")
        i = 1  # Initialize the counter for questions
        while i <= num_questions:
            time.sleep(1)
            print(f"Question {i}/{num_questions}:")
            question, answer = gen_qtn(level)
            print(f"Time limit: {time_limit[level_index]}seconds\nWhat is your answer for {question}")
            result = time_per_question(answer, time_limit[level_index])
            if result == 'quit':
                cont_game = "no"
                break
            if result==True:
                question_correct=question_correct+1
                score =score+ mark[level_index]
            i += 1  # Increment the question counter

        if cont_game == 'no':
            break


        print(f"You successfully answered {question_correct} questions correctly and your score is {score}")
        
        if level_index<2:
            cont_game = input("Do you want to continue the game? (yes/no): ").lower()
            if cont_game == "no":
                break
        else:
            break

        level_index += 1  # Move to the next level

    leaderboard=f"Math quiz score:{score}"

    if os.path.exists("data.json"):
        with open("data.json", "r") as file:
            data = json.load(file)  # Load existing data

    else:
        data = []

    data.append(leaderboard)


if __name__ == "__main__":
    math_quiz()
