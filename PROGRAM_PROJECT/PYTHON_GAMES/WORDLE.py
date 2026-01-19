import random
import os

# --- Configuration ---
MAX_TRIES = 5
WORD_LENGTH = 5

# ANSI Color Codes for the terminal
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'


def get_word_list():
    """Returns a small list of valid 5-letter words."""
    return [
        "APPLE", "BEACH", "BRAIN", "BREAD", "BRUSH",
        "CHAIR", "CHEST", "CHORD", "CLICK", "CLOCK",
        "CLOUD", "DANCE", "DIARY", "DRINK", "DRIVE",
        "EARTH", "FEAST", "FIELD", "FRUIT", "GLASS",
        "GRAPE", "GREEN", "GHOST", "HEART", "HOUSE",
        "JUICE", "LIGHT", "LEMON", "MELON", "MONEY",
        "MUSIC", "NIGHT", "OCEAN", "PARTY", "PIANO",
        "PILOT", "PHONE", "PLANE", "PLATE", "RADIO",
        "RIVER", "ROBOT", "SHIRT", "SHOES", "SMILE",
        "SNAKE", "SPACE", "SPOON", "STORM", "SUGAR",
        "TABLE", "TIGER", "TOAST", "TOUCH", "TRAIN",
        "TRUCK", "VOICE", "WASTE", "WATCH", "WATER",
        "WHALE", "WORLD", "WRITE", "YOUTH", "ZEBRA"
    ]


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def evaluate_guess(guess, secret):
    """
    Compares the guess with the secret word.
    Returns a list of formatted strings (colored letters).
    Logic:
    1. Identify exact matches (GREEN).
    2. Identify partial matches (YELLOW) handling duplicates correctly.
    3. The rest remain default (GRAY).
    """
    secret_list = list(secret)
    guess_list = list(guess)
    result = [""] * WORD_LENGTH

    # Pass 1: Find Greens (Correct Position)
    for i in range(WORD_LENGTH):
        if guess_list[i] == secret_list[i]:
            result[i] = f"{GREEN}{guess_list[i]}{RESET}"
            secret_list[i] = None  # Mark as used so it doesn't trigger Yellow later
            guess_list[i] = None  # Mark as processed

    # Pass 2: Find Yellows (Wrong Position)
    for i in range(WORD_LENGTH):
        if guess_list[i] is not None:  # Skip already marked Greens
            letter = guess_list[i]
            if letter in secret_list:
                result[i] = f"{YELLOW}{letter}{RESET}"
                # Remove *one* instance of this letter from secret to prevent double counting
                secret_list[secret_list.index(letter)] = None
            else:
                result[i] = letter  # No color (Gray/White)

    return "".join(result)


def main():
    clear_screen()
    print(f"=== PYTHON WORDLE ===")
    print(f"Guess the {WORD_LENGTH}-letter word in {MAX_TRIES} tries.")
    print(f"{GREEN}G{RESET} = Correct Spot, {YELLOW}Y{RESET} = Wrong Spot, White = Not in word")
    print("-" * 30)

    # Setup
    words = get_word_list()
    secret_word = random.choice(words)
    history = []

    # Game Loop
    for attempt in range(1, MAX_TRIES + 1):

        # Input Validation
        while True:
            guess = input(f"Attempt {attempt}/{MAX_TRIES}: ").upper()

            if len(guess) != WORD_LENGTH:
                print(f">> Word must be {WORD_LENGTH} letters long.")
                continue
            if not guess.isalpha():
                print(">> Letters only please.")
                continue
            break  # Input is valid

        # Process Guess
        colored_output = evaluate_guess(guess, secret_word)
        history.append(colored_output)

        # Display History (So user can see previous clues)
        clear_screen()
        print(f"=== PYTHON WORDLE ({attempt}/{MAX_TRIES}) ===")
        print("-" * 30)
        for line in history:
            print(f"  {line}")
        print("-" * 30)

        # Win Condition
        if guess == secret_word:
            print(f"\n🎉 EXCELLENT! You guessed '{secret_word}' in {attempt} tries.")
            break
    else:
        # Lose Condition (Loop finished without break)
        print(f"\n💀 GAME OVER. The word was '{secret_word}'.")


if __name__ == "__main__":
    main()