import random
import os
import time

# --- Data Setup ---
# A dictionary of countries mapped to their flag colors and continent
COUNTRIES = [
    {"name": "France", "colors": ["Blue", "White", "Red"], "continent": "Europe"},
    {"name": "Germany", "colors": ["Black", "Red", "Gold"], "continent": "Europe"},
    {"name": "Italy", "colors": ["Green", "White", "Red"], "continent": "Europe"},
    {"name": "Japan", "colors": ["White", "Red"], "continent": "Asia"},
    {"name": "Brazil", "colors": ["Green", "Yellow", "Blue", "White"], "continent": "South America"},
    {"name": "India", "colors": ["Saffron (Orange)", "White", "Green", "Blue"], "continent": "Asia"},
    {"name": "USA", "colors": ["Red", "White", "Blue"], "continent": "North America"},
    {"name": "Canada", "colors": ["Red", "White"], "continent": "North America"},
    {"name": "United Kingdom", "colors": ["Red", "White", "Blue"], "continent": "Europe"},
    {"name": "China", "colors": ["Red", "Yellow"], "continent": "Asia"},
    {"name": "Australia", "colors": ["Blue", "White", "Red"], "continent": "Oceania"},
    {"name": "South Africa", "colors": ["Red", "Blue", "Green", "Yellow", "Black", "White"], "continent": "Africa"},
    {"name": "Argentina", "colors": ["Light Blue", "White", "Gold"], "continent": "South America"},
    {"name": "Spain", "colors": ["Red", "Yellow"], "continent": "Europe"},
    {"name": "Sweden", "colors": ["Blue", "Yellow"], "continent": "Europe"},
    {"name": "Switzerland", "colors": ["Red", "White"], "continent": "Europe"},
    {"name": "Greece", "colors": ["Blue", "White"], "continent": "Europe"},
    {"name": "Mexico", "colors": ["Green", "White", "Red"], "continent": "North America"},
]

COLOR_EMOJIS = {
    "Red": "🔴", "Blue": "🔵", "Green": "🟢", "Yellow": "🟡",
    "Gold": "🟡", "White": "⚪", "Black": "⚫", "Orange": "🟠",
    "Saffron (Orange)": "🟠", "Light Blue": "💎"
}


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_color_display(color_list):
    """Converts a list of text colors into a string with emojis."""
    display = []
    for color in color_list:
        emoji = COLOR_EMOJIS.get(color, "🎨")
        display.append(f"{emoji} {color}")
    return ", ".join(display)


def main():
    score = 0
    rounds = 5
    random.shuffle(COUNTRIES)

    # Select first 5 for this session
    game_set = COUNTRIES[:rounds]

    clear_screen()
    print("=" * 40)
    print("🌍  GUESS THE COUNTRY BY FLAG COLORS  🌍")
    print("=" * 40)
    print(f"I will list the colors. You guess the nation.")
    input("Press [ENTER] to start...")

    for i, country in enumerate(game_set, 1):
        clear_screen()
        print(f"=== QUESTION {i}/{rounds} ===")
        print(f"Current Score: {score}")
        print("-" * 40)

        # Display Clue
        colors_str = get_color_display(country['colors'])
        print(f"FLAG COLORS:\n   {colors_str}")
        print("-" * 40)

        # Attempt Loop (3 Tries)
        solved = False
        target_name = country['name'].lower()

        for attempt in range(1, 4):
            # Hints logic
            hint = ""
            if attempt == 2:
                hint = f"(Hint: Starts with '{country['name'][0]}')"
            elif attempt == 3:
                hint = f"(Hint: Located in {country['continent']})"

            # Input
            guess = input(f"Attempt {attempt}/3 {hint}: ").strip().lower()

            # Check Answer
            if guess == target_name or (target_name == "usa" and guess in ["united states", "america"]):
                print(f"\n✅ Correct! It is {country['name']}.")
                score += 1
                solved = True
                time.sleep(1.5)
                break
            else:
                if attempt < 3:
                    print("❌ Wrong. Try again.")
                else:
                    print(f"\n💀 Out of tries! The answer was: {country['name']}")
                    time.sleep(2)

    # End Game
    clear_screen()
    print("=" * 40)
    print("🎉  QUIZ COMPLETE  🎉")
    print(f"Your Final Score: {score}/{rounds}")

    if score == rounds:
        print("Rank: GEOGRAPHY GENIUS 🌍")
    elif score >= rounds // 2:
        print("Rank: TRAVELLER ✈️")
    else:
        print("Rank: TOURIST 📷")
    print("=" * 40)


if __name__ == "__main__":
    main()