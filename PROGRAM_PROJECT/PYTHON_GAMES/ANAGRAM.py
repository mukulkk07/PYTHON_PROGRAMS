import random
import os
import time

# --- Game Data ---
# Format: "WORD": "Definition/Hint"
WORDS = {
    "EASY": {
        "LION": "The king of the jungle.",
        "READ": "Looking at text and understanding it.",
        "JUMP": "To push yourself into the air.",
        "BLUE": "The color of the sky.",
        "FISH": "An animal that lives underwater.",
        "CAKE": "A sweet baked food.",
        "SONG": "Music with words.",
        "MILK": "White liquid from cows."
    },
    "MEDIUM": {
        "PLANET": "A large object orbiting a star.",
        "GUITAR": "A musical instrument with strings.",
        "SUMMER": "The hottest season of the year.",
        "FOREST": "A large area covered with trees.",
        "MARKET": "A place where people buy and sell.",
        "DOCTOR": "Someone who treats sick people.",
        "WINDOW": "An opening in a wall to see outside.",
        "YELLOW": "The color of lemons and the sun."
    },
    "HARD": {
        "PYRAMID": "A monumental structure with a square base.",
        "JOURNEY": "Traveling from one place to another.",
        "LIBRARY": "A place containing collections of books.",
        "UNKNOWN": "Something that is not discovered.",
        "BALANCE": "An even distribution of weight.",
        "CAPTAIN": "The person in command of a ship.",
        "VILLAGE": "A group of houses, smaller than a town.",
        "MYSTERY": "Something that is difficult to explain."
    }
}


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def scramble_word(word):
    """Returns a shuffled version of the word."""
    word_list = list(word)
    shuffled = word_list[:]

    # Keep shuffling until it's different from the original
    while shuffled == word_list:
        random.shuffle(shuffled)

    return "".join(shuffled)


def get_difficulty():
    while True:
        clear_screen()
        print("=== WORD SCRAMBLE ===")
        print("1. Easy (4 letters)")
        print("2. Medium (6 letters)")
        print("3. Hard (7+ letters)")
        choice = input("Select Difficulty (1-3): ")

        if choice == '1': return "EASY"
        if choice == '2': return "MEDIUM"
        if choice == '3': return "HARD"


def main():
    difficulty = get_difficulty()
    word_pool = list(WORDS[difficulty].keys())
    random.shuffle(word_pool)

    score = 0
    rounds = 5
    game_words = word_pool[:rounds]  # Play 5 rounds

    print(f"\nStarting {difficulty} Mode! Unscramble the letters.")
    print("Type 'HINT' for a clue (-2 points).")
    input("Press [ENTER] to begin...")

    for i, target_word in enumerate(game_words, 1):
        scrambled = scramble_word(target_word)
        definition = WORDS[difficulty][target_word]
        attempts = 3
        hint_used = False

        while attempts > 0:
            clear_screen()
            print(f"=== ROUND {i}/{rounds} | Score: {score} ===")
            print(f"Scrambled:  [ {scrambled} ]")

            if hint_used:
                print(f"HINT: {definition}")

            guess = input(f"Your Guess ({attempts} tries left): ").upper().strip()

            if guess == "HINT":
                if not hint_used:
                    hint_used = True
                    score -= 2
                    print(">> Hint revealed! Points deducted.")
                    time.sleep(1)
                else:
                    print(">> You already used the hint!")
                    time.sleep(1)
                continue

            if guess == target_word:
                print(f"\n✅ Correct! The word was {target_word}.")
                points = 10
                if hint_used: points -= 2  # Penalty already applied to score, but this adjusts round logic if needed
                score += 10
                time.sleep(1.5)
                break
            else:
                attempts -= 1
                print("❌ Incorrect.")
                time.sleep(0.8)

        if attempts == 0:
            print(f"\n💀 Out of tries! The word was {target_word}.")
            time.sleep(2)

    # End Game
    clear_screen()
    print("=" * 30)
    print(f"🎉 GAME FINISHED! 🎉")
    print(f"Final Score: {score}")
    print("=" * 30)


if __name__ == "__main__":
    main()