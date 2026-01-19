import random
import os
import time


def clear_screen():
    """Clears the console screen based on the operating system."""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_hangman_stages():
    """Returns a list of ASCII art representing the hangman stages."""
    return [
        """
           ------
           |    |
           |
           |
           |
           |
        --------
        """,
        """
           ------
           |    |
           |    O
           |
           |
           |
        --------
        """,
        """
           ------
           |    |
           |    O
           |    |
           |
           |
        --------
        """,
        """
           ------
           |    |
           |    O
           |   /|
           |
           |
        --------
        """,
        """
           ------
           |    |
           |    O
           |   /|\\
           |
           |
        --------
        """,
        """
           ------
           |    |
           |    O
           |   /|\\
           |   /
           |
        --------
        """,
        """
           ------
           |    |
           |    O
           |   /|\\
           |   / \\
           |
        --------
        """
    ]


def get_random_word():
    """Returns a random word from a predefined list."""
    words = [
        "PYTHON", "DEVELOPER", "ALGORITHM", "KEYBOARD", "PROCESSOR",
        "DATABASE", "VARIABLE", "FUNCTION", "INTERFACE", "COMPILER",
        "FRAMEWORK", "DEBUGGING", "SYNTAX", "BACKEND", "FRONTEND"
    ]
    return random.choice(words)


def display_game_state(tries, hidden_word, guessed_letters):
    """
    Visualizes the current state of the game.
    """
    stages = get_hangman_stages()

    # Calculate which stage to show (0 is empty, 6 is full hangman)
    # We have 6 tries.
    # 6 tries left = index 0
    # 0 tries left = index 6
    stage_index = 6 - tries

    print(stages[stage_index])
    print(f"Word: {hidden_word}")
    print(f"\nGuessed: {', '.join(sorted(guessed_letters))}")
    print(f"Lives remaining: {tries}")
    print("-" * 30)


def main():
    word_to_guess = get_random_word()
    guessed_letters = set()
    tries = 6
    won = False

    while tries > 0:
        clear_screen()

        # Build the hidden word string (e.g., "P _ T _ O N")
        display_word = [letter if letter in guessed_letters else "_" for letter in word_to_guess]
        display_word_str = " ".join(display_word)

        # Check win condition before getting input
        if "_" not in display_word:
            won = True
            display_game_state(tries, display_word_str, guessed_letters)
            break

        display_game_state(tries, display_word_str, guessed_letters)

        # Input handling
        guess = input("Guess a letter: ").upper()

        # Validation logic
        if not guess.isalpha() or len(guess) != 1:
            print(">> Please enter a single alphabetic character.")
            time.sleep(1.5)  # Pause so user can read the error
            continue

        if guess in guessed_letters:
            print(f">> You already guessed '{guess}'. Try again.")
            time.sleep(1.5)
            continue

        guessed_letters.add(guess)

        if guess in word_to_guess:
            print(f">> Good job! '{guess}' is in the word.")
            time.sleep(1)
        else:
            print(f">> Sorry, '{guess}' is not there.")
            tries -= 1
            time.sleep(1)

    # Game Over Logic
    clear_screen()
    display_game_state(tries, display_word_str if won else " ".join(["_" for _ in word_to_guess]), guessed_letters)

    if won:
        print("\n🎉 CONGRATULATIONS! You saved the hangman! 🎉")
    else:
        print("\n💀 GAME OVER! 💀")
        print(f"The word was: {word_to_guess}")


if __name__ == "__main__":
    main()