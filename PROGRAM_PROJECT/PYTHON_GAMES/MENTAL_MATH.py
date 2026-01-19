import random
import time
import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def generate_question(score):
    """
    Generates a math problem based on current score (difficulty).
    Returns: tuple (question_string, correct_answer)
    """
    operators = ['+', '-', '*']

    # Increase number range slightly as you progress
    max_val = 10 + int(score * 1.5)

    a = random.randint(2, max_val)
    b = random.randint(2, max_val)
    op = random.choice(operators)

    # Ensure subtraction doesn't result in negative numbers (for simplicity)
    if op == '-' and a < b:
        a, b = b, a

    # Ensure multiplication isn't too huge
    if op == '*':
        a = random.randint(2, 12)
        b = random.randint(2, 12)

    question = f"{a} {op} {b}"
    answer = eval(question)  # Safe here since we control the string
    return question, answer


def countdown():
    print("Get Ready...")
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(0.8)
    print("GO!\n")


def main():
    clear_screen()
    print("=" * 40)
    print("⚡  QUICK MENTAL MATH CHALLENGE  ⚡")
    print("=" * 40)
    print("RULES:")
    print("1. Solve the problem shown.")
    print("2. You have exactly 5 SECONDS per question.")
    print("3. If you are slow OR wrong, Game Over.")
    print("-" * 40)

    input("Press [ENTER] to start...")
    clear_screen()
    countdown()

    score = 0
    time_limit = 5.0

    while True:
        # 1. Generate Question
        q_str, correct_ans = generate_question(score)

        print(f"Question {score + 1}:")
        print(f"   {q_str} = ?")

        # 2. Start Timer
        start_time = time.time()

        # 3. Get Input
        try:
            user_input = input("   Answer: ")
        except ValueError:
            print("\n>> Invalid input! Game Over.")
            break

        # 4. Stop Timer
        end_time = time.time()
        time_taken = end_time - start_time

        # 5. Validate Time
        if time_taken > time_limit:
            print(f"\n❌ TOO SLOW! You took {time_taken:.2f} seconds.")
            print(f"The limit was {time_limit} seconds.")
            break

        # 6. Validate Answer
        try:
            val = int(user_input)
        except ValueError:
            print(f"\n❌ That's not a number! Game Over.")
            break

        if val == correct_ans:
            print(f"✅ Correct! ({time_taken:.2f}s)\n")
            score += 1
            # Add a tiny pause so the user can blink
            time.sleep(0.5)
        else:
            print(f"\n❌ WRONG! The answer was {correct_ans}.")
            break

    # End Game
    print("-" * 40)
    print(f"💀 GAME OVER 💀")
    print(f"Final Score: {score}")

    # Custom rating
    if score > 20:
        print("Rank: HUMAN CALCULATOR 🧠")
    elif score > 10:
        print("Rank: Math Whiz ⚡")
    elif score > 5:
        print("Rank: Rookie 🎓")
    else:
        print("Rank: Needs Practice 🐢")
    print("=" * 40)


if __name__ == "__main__":
    main()