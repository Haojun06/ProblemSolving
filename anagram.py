import random
import time
import os
import json
import requests


# Clear the terminal screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# Load words by using API
def load_words():
    try:
        url = "https://random-word-api.p.rapidapi.com/L/5"      #API endpoint to get words with 5 letters
        headers = {
            "x-rapidapi-host": "random-word-api.p.rapidapi.com",  #API host
            "x-rapidapi-key": "a39affc583mshb5f4b5ede89a1bap1d3bb4jsncd1c1b704b7e" #API key
        }


        response = requests.get(url,headers=headers)  #make a get request to the API
        if response.status_code == 200:
            data = response.json()  # API returns a list of words
            
            if isinstance(data, dict) and "word" in data: #check if the data is a dictionary and has the key "word"
                return [data["word"]]  # Extract word from dictionary
            elif isinstance(data, list):   #check if the data is a list
                return data  # If the API returns a list, use it directly
        else:  #if the status code is not 200
            print("Error fetching words from API. Using fallback words.")
            return ["default", "example", "random", "python", "coding"]
    except requests.RequestException:  #if there is an error with the request(e.g. network error)
        print("Network error. Using fallback words.")
        return ["default", "example", "random", "python", "coding"]



# Shuffle the word
def shuffle_word(word):
    word_list = list(word) #convert the word to a list
    random.shuffle(word_list) #shuffle the list
    return ''.join(word_list) #join the list back to a string


# Load scores from JSON file
def load_scores():
    try:
        with open("scores.json", "r") as file:  #open the scores.json file in read mode
            data = json.load(file)  #load the data from the file
            if isinstance(data, list):      #check if the data is a list
                return data #return the data
            else:   #if the data is not a list
                return []   #return an empty list
    except (FileNotFoundError, json.JSONDecodeError): #if the file is not found or there is a JSON decode error
        return []  #return an empty list


# Save scores to JSON file
def save_scores(data):
    with open("scores.json", "w") as file: #open the scores.json file in write mode
        json.dump(data, file, indent=4) #write the data to the file with indentation


# Show leaderboard
def show_anagramleaderboard(): 
    if os.path.exists("scores.json"):  #check if the scores.json file exists
        with open("scores.json", "r") as file:  #open the scores.json file in read mode
            data = json.load(file)      #load the data from the file
        if data: #if there is data in the file
            print("\n🏆 Anagram Leaderboard 🏆")    
            # Sort the data by score in descending order and get the top 5 scores
            top_scores = sorted(data, key=lambda x: x["score"], reverse=True)[:5]  
            for i, entry in enumerate(top_scores):  #iterate over the top scores
                print(f"{i + 1}. {entry['username']}: {entry['score']}")
        else:
            print("No scores yet. Be the first to set a high score!")
    else:
        print("No scores yet. Be the first to set a high score!")


# Main menu
def main_menu():
    while True:
        clear_screen()
        # Display the main menu options
        print("Welcome to the Advanced Anagram Game!\n")
        print("1. Play Timed Mode")
        print("2. Play Relaxed Mode")
        print("3. View Scores")
        print("4. View Leaderboard")
        print("5. Quit\n")

        choice = input("Choose an option: ").strip()
        # Check the user's choice and call the corresponding function
        if choice == "1":
            play_timed_mode()
        elif choice == "2":
            play_relaxed_mode()
        elif choice == "3":
            view_scores()
            input("\nPress Enter to return to the main menu.")
        elif choice == "4":
            show_anagramleaderboard()
            input("\nPress Enter to return to the main menu.")
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
            time.sleep(2)


# View high scores
def view_scores():
    scores = load_scores()
    clear_screen()
    print("High Scores:\n")
    if scores:
        for entry in scores:
            # Display the username, score, hints used, and rounds played for each entry
            print(f"Username: {entry['username']}, Score: {entry['score']}, Hints Used: {entry['hints_used']}, Rounds Played: {entry['rounds_played']}")
    else:
        print("No scores available.")
    input("Press Enter to return to the main menu.")


def play_timed_mode():
    scores = load_scores()  # Load scores from file
    print("Starting Timed Mode...\n")
    print("Rules: Unscramble the letters to form a valid word.")
    print("Type 'hint' for a hint, 'skip' to skip a word, or 'quit' to exit.\n")

    # Check if there are existing scores and display the high score
    if not scores or not all(isinstance(score, dict) and 'score' in score for score in scores):
        print("No high scores yet. Be the first to set a high score!")
        high_score = 0
    else:
        high_score = max(scores, key=lambda x: x['score'])['score']  

    input(f"Current High Score: {high_score}\nPress Enter to continue...")

    score = 0
    hints_used = 0
    rounds_played = 0
    max_game_time = 30  # Set total game time limit
    start_time = time.time()
 
    # Loop until the game time limit is reached
    while time.time() - start_time < max_game_time:
        words = load_words()  # Load new words for each round
        clear_screen()
        word = random.choice(words) # Select a random word
        scrambled = shuffle_word(word)

        print(f"Round {rounds_played + 1}: Scrambled word: {scrambled}\n")
        print(f"Time left: {max_game_time - (time.time() - start_time):.2f} seconds") # Display remaining time

        attempts = 3
        while attempts > 0:
            guess = input(f"Your guess (Attempts left: {attempts}): ").strip().lower() # Get user input

            # Check if the user wants to quit, get a hint, or skip the word
            if guess == "quit":
                clear_screen()
                print(f"Thanks for playing!\n\nYour final score: {score}\nHints used: {hints_used}\nTotal rounds played: {rounds_played}\n")
                save_scores(scores)
                return

            if guess == "hint":
                print(f"Hint: The word starts with '{word[0]}' and ends with '{word[-1]}'.")
                hints_used += 1
                continue

            if guess == "skip":
                print(f"The word was: {word}. Moving to the next word.\n")
                input("\nPress Enter to continue...")
                break

            if guess == word:
                score += 1
                rounds_played += 1
                print(f"Correct! Well done!\n")
                input("\nPress Enter to continue...")
                break
            else:
                attempts -= 1
                if attempts > 0:
                    print("Incorrect. Try again!")
                else:
                    print(f"Out of attempts! The word was: {word}.\n")

    username = input("Enter your username: ").strip()
    # Add the user's score, hints used, and rounds played to the scores list
    scores.append({"username": username, "score": score, "hints_used": hints_used, "rounds_played": rounds_played})
    save_scores(scores)


# Relaxed mode
def play_relaxed_mode():
    # Load scores from file
    scores = load_scores()
    print("Starting Timed Mode...\n")
    print("Rules: Unscramble the letters to form a valid word.")
    print("Type 'hint' for a hint, 'skip' to skip a word, or 'quit' to exit.\n")

    # Check if there are existing scores and display the high score
    if not scores or not all(isinstance(score, dict) and 'score' in score for score in scores):
        print("No high scores yet. Be the first to set a high score!")
        high_score = 0
    else:
        high_score = max(scores, key=lambda x: x['score'])['score']

    input(f"Current High Score: {high_score}\nPress Enter to continue...")

    score, hints_used, rounds_played = 0, 0, 0

    while True:
        words = load_words()  # Load new words for each round
        clear_screen()
        word = random.choice(words)
        scrambled = shuffle_word(word)
        print(f"Round {rounds_played + 1}: Scrambled word: {scrambled}\n")

        guess = input("Your guess (or 'quit' to exit): ").strip().lower()
        
        # Check if the user wants to quit, get a hint, or skip the word
        if guess == "quit":
            break

        if guess == "hint":
            print(f"Hint: The word starts with '{word[0]}' and ends with '{word[-1]}'.")
            hints_used += 1
            input("Press Enter to continue...")  # Pause after displaying the hint
            continue

        if guess == word:
            score += 1
            print("Correct! Well done!\n")
        else:
            print(f"Incorrect. The word was: {word}\n")

        rounds_played += 1
        input("\nPress Enter to continue...")

    username = input("Enter your username: ").strip()
    scores.append({"username": username, "score": score, "hints_used": hints_used, "rounds_played": rounds_played})
    save_scores(scores)
    save_scores(scores)


if __name__ == "__main__":
    main_menu()
