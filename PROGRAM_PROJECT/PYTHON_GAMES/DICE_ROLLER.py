import random
import os
import time


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_die_face(number):
    """Returns a list of strings representing the ASCII art of a die face."""
    faces = {
        1: [
            "+-------+",
            "|       |",
            "|   o   |",
            "|       |",
            "+-------+"
        ],
        2: [
            "+-------+",
            "| o     |",
            "|       |",
            "|     o |",
            "+-------+"
        ],
        3: [
            "+-------+",
            "| o     |",
            "|   o   |",
            "|     o |",
            "+-------+"
        ],
        4: [
            "+-------+",
            "| o   o |",
            "|       |",
            "| o   o |",
            "+-------+"
        ],
        5: [
            "+-------+",
            "| o   o |",
            "|   o   |",
            "| o   o |",
            "+-------+"
        ],
        6: [
            "+-------+",
            "| o   o |",
            "| o   o |",
            "| o   o |",
            "+-------+"
        ]
    }
    return faces[number]


def roll_dice_animation():
    """Simulates a rolling effect."""
    print("Rolling...")
    time.sleep(0.5)
    print("Clatter...")
    time.sleep(0.5)
    clear_screen()


def print_dice_side_by_side(dice_values):
    """Prints multiple dice faces horizontally next to each other."""
    # Get the ASCII art for each die value
    faces = [get_die_face(val) for val in dice_values]

    # We zip the faces so we print line 1 of all dice, then line 2, etc.
    # zip(*faces) takes the 1st row of die 1, 1st row of die 2, etc.
    for lines in zip(*faces):
        print("  ".join(lines))


def main():
    clear_screen()
    print("=== TRIPLE DICE ROLLER ===")
    print("Press [ENTER] to roll the dice.")
    print("Type 'exit' or 'q' to quit.")

    while True:
        user_input = input("\n> ").lower().strip()

        if user_input in ['exit', 'quit', 'q']:
            print("Thanks for playing!")
            break

        roll_dice_animation()

        # 1. Generate Random Numbers
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        d3 = random.randint(1, 6)

        dice_values = [d1, d2, d3]
        total_sum = sum(dice_values)

        # 2. Display Visuals
        print(f"You rolled: {d1}, {d2}, {d3}\n")
        print_dice_side_by_side(dice_values)

        # 3. Display Sum
        print("-" * 30)
        print(f"🎲  TOTAL SUM: {total_sum}  🎲")
        print("-" * 30)


if __name__ == "__main__":
    main()