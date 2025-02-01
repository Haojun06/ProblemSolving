import random
import time
import os
import json
import requests

# Shuffle the word
def shuffle_word(word):
    word_list = list(word)
    random.shuffle(word_list)
    return ''.join(word_list)

# Load words by using api
def load_words():
    try:
        url = "https://random-word-api.p.rapidapi.com/L/5"  
        headers = {
            "x-rapidapi-host": "random-word-api.p.rapidapi.com",
            "x-rapidapi-key": "a39affc583mshb5f4b5ede89a1bap1d3bb4jsncd1c1b704b7e"
        }


        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            data = response.json()  # API returns a list of words
            
            if isinstance(data, dict) and "word" in data:
                return [data["word"]]  # Extract word from dictionary
            elif isinstance(data, list):
                return data  # If the API returns a list, use it directly
        else:
            print("Error fetching words from API. Using fallback words.")
            return ["default", "example", "random", "python", "coding"]
    except requests.RequestException:
        print("Network error. Using fallback words.")
        return ["default", "example", "random", "python", "coding"]




# Clear the terminal screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Load scores from a JSON file
def load_scores():
    try:
        with open("scores.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"high_score": 0, "hints_used": 0, "rounds_played": 0}

# Save scores to a JSON file
def save_scores(data):
    with open("scores.json", "w") as file:
        json.dump(data, file, indent=4)

# Main menu
def main_menu():
    while True:
        clear_screen()
        print("Welcome to the Advanced Anagram Game!\n")
        print("1. Play Timed Mode")
        print("2. Play Relaxed Mode")
        print("3. View Scores")
        print("4. Quit\n")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            play_anagram_game(timed=True)
        elif choice == "2":
            play_anagram_game(timed=False)
        elif choice == "3":
            view_scores()
        elif choice == "4":
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
    print(f"High Score: {scores['high_score']}")
    print(f"Hints Used: {scores['hints_used']}")
    print(f"Total Rounds Played: {scores['rounds_played']}\n")
    input("Press Enter to return to the main menu.")

# Play the anagram game
def play_anagram_game(timed):
    words = load_words()
    
    if not words:
        print("Error: No words available to play. Exiting.")
        return

    scores = load_scores()
    print(f"Starting {'Timed' if timed else 'Relaxed'} Mode...\n")
    print("Rules: Unscramble the letters to form a valid word.")
    print("Type 'hint' for a hint, 'skip' to skip a word, or 'quit' to exit.\n")
    input(f"Current High Score: {scores['high_score']}\nPress Enter to continue...")

    score = 0
    hints_used = 0
    rounds_played = 0
    global_timer = 0  # Track total time for game session
    max_game_time = 30  # Set total game time limit

    while global_timer < max_game_time:
        words = load_words()
        clear_screen()
        word = random.choice(words)  # Pick a random word for the round
        scrambled = shuffle_word(word)  # Shuffle the word to make it an anagram

        print(f"Round {rounds_played + 1}: Scrambled word: {scrambled}\n")

        attempts = 3
        round_start_time = time.time()

        while attempts > 0:
            elapsed_time = time.time() - round_start_time
            global_timer += elapsed_time  
            round_start_time = time.time()


            # Check if the overall game timer has expired
            if global_timer >= max_game_time:
                print("\nTime's up! You have reached the 30-second game limit.")
                print(f"Final Score: {score}\nHints used: {hints_used}\nTotal rounds played: {rounds_played}\n")
                if score > scores["high_score"]:
                    print(f"New High Score! Previous High Score: {scores['high_score']}\n")
                    scores["high_score"] = score
                scores["hints_used"] += hints_used
                scores["rounds_played"] += rounds_played
                save_scores(scores)
                return

            print(f"Time left: {max_game_time - global_timer:.2f} seconds")

            guess = input(f"Your guess (Attempts left: {attempts}): ").strip().lower()

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

            if guess.lower() == word.lower():
                end_time = time.time()
                round_time = end_time - round_start_time
                global_timer += round_time
                score += 1
                rounds_played += 1
                print(f"Correct! Well done!\nTime taken: {round_time:.2f} seconds\n")
                input("\nPress Enter to continue...")
                break
            else:
                end_time = time.time()
                round_time = end_time - round_start_time
                global_timer += round_time
                score -= 1
                rounds_played += 1
                print("Incorrect word. Do you want to:")
                print("1. Try again")
                print("2. Move to the next word")
                option = input("Choose an option (1/2): ").strip()

                if option == "2":
                    print(f"The correct word was: {word}. Moving to the next word.\n")
                    input("\nPress Enter to continue...")
                    break
                else:
                    print("Try again!")
                    attempts -= 1

        if attempts <= 0:
            print(f"Out of attempts! The word was: {word}.\n")
            print(f"Rounds played: {rounds_played}\n")
            print(f"Your score is {score}")
            input("\nPress Enter to continue...")
            
            rounds_played += 1

        if global_timer < max_game_time:
            print(f"Out of time! \n")
            print(f"Rounds played: {rounds_played}\n")
            print(f"Your score is {score}")
            input("Press Enter to continue...")
if __name__ == "__main__":
    main_menu()
