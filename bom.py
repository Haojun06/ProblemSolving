import random
import time
import os
import json


# Function to set up a random correct answer and fake hint turn
def setting (level):
    global correct , fake_hint_turn #let the value declares to whole program
    fake_hint_turn = random.randint(1, 6) # randomly set a fake hint turn
    correct = random.randint(1,level) #random correct number 
    print(f"The correct number is between 1 and {level}")
    
#Function to decrease the lives and give the fake hint or real hint
def hint(guess):
    global lives #let the value declares to whole program
    lives -=  1 #decreasing the number of lives after each guess
    if lives == fake_hint_turn - 1:#if the random number(fake_hint_turn) is equal to the lives , fake hint is triggered
        if correct > guess:
            print (f"smaller than {guess}...lives remain :{lives}")
        else :
            print (f"greater than {guess}...lives remain :{lives}")
    else:# If it's a real hint
        if correct > guess:
            print (f"greater than {guess}...lives remain :{lives}")
        else: print (f"smaller  than {guess}...lives remain :{lives}")
    return lives # Returning the remaining lives after each guess
    
#Function to show result of guess
def result(score,guess,streak):
    if correct == guess: # If the guess is correct
        print("CORRECT ANSWER !! GO TO NEXT LEVEL")
        score += 100 # adding score
        streak += 1 # adding streak
        if streak == 4 : 
            score *= 2 # if streak is enough ,double the score
            print("BONUS:scores is doubled") 
            print(f"current score = {score}")
            streak = 0 # reset the streak 
        status = "next" 
        clear_screen()# Clears the screen before each question
    else:
        print(f"GAME OVER . The correct number was {correct}.")
        status = "stop"
        time.sleep(2) # Pause so user can see "GAME OVER"
    return score , status ,streak

#Function to show level difficulty
def levels(level):
    if level <= 10 :
        print("level : EASY ")
    elif level <= 20 and level >10:
        print("level : HARD ")
    elif level <= 30 and level >20:
        print("level : DIFFICULT ")
    else:
        print("level : INSANE ")

def save_score(score):
    if os.path.exists("bombscore.json"):
        try:
            with open("bombscore.json", "r") as file: #open the file in read mode
                data = json.load(file)# Load existing scores
        except json.JSONDecodeError: # Handle the case where the JSON file is corrupted
            print("⚠️ Warning: Score file is corrupt. Resetting scores.")
            data = []  # Reset to an empty list if the file is corrupted
    else:
        data = []  # If no file, start fresh

    data.append({"score": score})  # Store score as a dictionary

    with open("bombscore.json", "w") as file:
        json.dump(data, file)  # Save updated scores
        
#Function to show leaderboard before start
def show_leaderboard():
    if os.path.exists("bombscore.json"):# If the score file exists
        with open("bombscore.json", "r") as file:
            data = json.load(file)  # Load existing scores

        if data: # If there are scores
            print("\n🏆 Math Bomb Leaderboard 🏆")
            top_scores = sorted(data, key=lambda x: x["score"], reverse=True)[:5]  # Show top 5
            for i, entry in enumerate(top_scores):
                print(f"{i+1}. Score: {entry['score']}")
        else:
            print("No scores yet. Be the first to set a high score!")
    else:
        print("No scores yet. Be the first to set a high score!")

#Function to clear the screen
def clear_screen():
    time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')  # Clears screen for Windows (cls) and macOS/Linux (clear)
    
# Function to ask the player if they want to continue
def ask_continue():
    while True:
        choice = input("Do you want to continue playing? (yes/no): ").strip().lower()  # ensure no spacing and case-insensitivity
        if choice == "no":
            return "stop"  # Return "stop" to end the game
        elif choice == "yes":
            return "next"  # Return "next" to continue the game
        else:
            print("Invalid choice. Please enter 'yes' or 'no'.")

def math_bomb():
    global lives

    #starting part
    print("Welcome to MATH BOMB section ^-^")
    time.sleep(1) # delay for better user experience
    print("You will be given 6 lives for guessing the correct answer")
    time.sleep(1)
    print("Hint will be given after a wrong answer , but there will be one fake hint.")
    time.sleep(1)
    print("🔥 Hit a streak of 3 correct answers and earn a 2x bonus !")
    time.sleep(1)

    #setting a initial value 
    level = 0 # Starting level of the game
    score = 0 # Player's score
    status = "next" # Game status (next means the game continues)
    lives = 6 #PLayer's lives
    streak = 0 #streak in correct answer

    # Call this before the game starts to show the leaderboard
    show_leaderboard() 
    time.sleep(1)

    #Game loop
    while status == "next":
        lives = 6 # Reset lives to 6 for each new round
        level += 10 # Increase level after each round
        setting(level) # Set the correct answer and fake hint turn for the round
        levels(level) # Display the current difficulty level
        print(f"Your current score: {score}")
        print(f"Your current streak: {streak}")

        guess = None
        while guess is None:
            try:
                guess = int(input("Your Guess: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                
        # Keep giving hints until the player guesses correctly or runs out of lives       
        while guess != correct and lives > 0 :
            lives = hint(guess) # Call the hint function and decrease lives
            if lives > 0: # If the player still has lives, ask for another guess
                guess = None 
                while guess is None :
                    try:
                        guess = int(input("Your Guess: "))
                    except ValueError:
                        print("Invalid input. Please enter a number.")
        

                    
        score ,status,streak = result(score,guess,streak)

        
        # Every 4 levels, ask the player if they want to continue
        if level % 40 == 0 and status == "next":
            print("\n🎮 You've completed 4 levels! 🎮")
            status = ask_continue()  # Use the function to ask if the player wants to continue

        
    # Save score at the end of the game
    print(f"Your final score is: {score}")
    save_score(score)
        
    # Show updated leaderboard after the game
    show_leaderboard()

    # Pause for 5 seconds so user can see the final score
    time.sleep(5) 

if __name__ == "__main__":
    math_bomb()
