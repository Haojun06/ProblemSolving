import random
import time
import os
import json

#starting part
print("Welcome to MATH BOMB section ^-^")
time.sleep(1)
print("You will be given 6 lives for guessing the correct answer")
time.sleep(1)
print("Hint will be given after a wrong answer , but there will be one fake hint.")
time.sleep(1)

#setting a initial value 
level = 0
score = 0
status = "next"

#setting a correct answer and fake hint round
def setting ():
    global correct , fake_hint_turn #let the value declares to whole program
    fake_hint_turn = random.randint(1, 6)
    correct = random.randint(1,level)
    print(f"The correct number is between 1 and {level}")
    
#decrease the lives and give the fake hint or real hint
def hint(guess):
    global lives 
    lives -=  1
    if lives == fake_hint_turn - 1:#if the random number(fake_hint_turn) is equal to the lives , fake hint come out
        if correct > guess:
            print (f"smaller than {guess}...lives remain :{lives}")
        else :
            print (f"greater than {guess}...lives remain :{lives}")
    else:
        if correct > guess:
            print (f"greater than {guess}...lives remain :{lives}")
        else: print (f"smaller  than {guess}...lives remain :{lives}")
    return lives
    

def result(guess):
    global score , status
    if correct == guess:
        print("CORRECT ANSWER !! GO TO NEXT LEVEL")
        score += 100
        status = "next"
    else:
        print(f"GAME OVER . The correct number was {correct}.")
        status = "stop"

#showing level difficulty
def levels(level):
    if level <= 10 :
        print("level : EASY ")
    elif level <= 20 and level >10:
        print("level : HARD ")
    elif level <= 30 and level >20:
        print("level : DIFFICULT ")
    else:
        print("level : INSANE ")

# Save the score
def save_score(score):
    if os.path.exists("bombscore.json"):
        try:
            with open("bombscore.json", "r") as file:#open the file in read mode
                data = json.load(file)# Load existing scores
        except json.JSONDecodeError:
            print("⚠️ Warning: Score file is corrupt. Resetting scores.")
            data = []  # Reset to an empty list if the file is corrupted
    else:
        data = []  # If no file, start fresh

    data.append({"score": score})  # Store score as a dictionary

    with open("bombscore.json", "w") as file:
        json.dump(data, file)  # Save updated scores
        
#show leaderboard before start
def show_leaderboard():
    if os.path.exists("bombscore.json"):
        with open("bombscore.json", "r") as file:
            data = json.load(file)

        if data:
            print("\n🏆 Math Bomb Leaderboard 🏆")
            top_scores = sorted(data, key=lambda x: x["score"], reverse=True)[:5]  # Show top 5
            for i, entry in enumerate(top_scores):
                print(f"{i+1}. Score: {entry['score']}")
        else:
            print("No scores yet. Be the first to set a high score!")
    else:
        print("No scores yet. Be the first to set a high score!")

        
# Call this before the game starts
show_leaderboard() 
time.sleep(1)

#Game loop
while status == "next":
    lives = 6
    level += 10
    setting()
    levels(level)
    while True :
        try:
            guess = int(input("Your Guess: "))
            
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
            
    while guess != correct and lives > 0 :
        lives = hint(guess)
        if lives > 0:
            try:
                guess = int(input("Your Guess: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                
    result(guess)

    
    #Every 4 levels, ask the player if they want to continue
    if level % 40 == 0 and status == "next":  
        print("\n🎮 You've completed 4 levels! 🎮")
        while True:
            choice = input("Do you want to continue playing? (yes/no): ").lower()
            if choice == "no":
                status = "stop"
                break
            elif choice == "yes":
                break
            else:
                print("Invalid choice. Please enter 'yes' or 'no'.")
    
# Save score at the end of the game
print(f"Your final score is: {score}")
save_score(score)
    
# Show updated leaderboard after the game
show_leaderboard()
