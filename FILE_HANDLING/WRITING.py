"""
Python File Writing Tutorial
============================
This script demonstrates various methods to write data to a .txt file in Python.

Key Concepts Covered:
1. The 'with' statement (Context Managers) for safe file handling.
2. 'w' mode: Write (Overwrites existing data).
3. 'a' mode: Append (Adds to the end of the file).
4. 'x' mode: Exclusive creation (Fails if file exists).
5. Writing lists of strings.
6. Handling encoding (UTF-8).
"""

import os

# Define a filename to use for this demonstration
FILENAME = "demo_output.txt"


def write_basic_mode():
    """
    Demonstrates the basic 'w' (write) mode.
    WARNING: This mode completely overwrites the file if it exists.
    """
    print(f"--- 1. Writing to {FILENAME} in 'w' mode ---")

    # The 'with' statement automatically closes the file after the block ends.
    # encoding='utf-8' ensures special characters are handled correctly.
    with open(FILENAME, mode='w', encoding='utf-8') as file:
        file.write("Hello! This is the first line.\n")
        file.write("This file was created using Python.\n")
        file.write("Note: 'w' mode wiped any previous content.\n")

    print("-> Successfully wrote initial data.\n")


def append_mode():
    """
    Demonstrates the 'a' (append) mode.
    This adds data to the end of the file without deleting existing content.
    """
    print(f"--- 2. Appending to {FILENAME} in 'a' mode ---")

    with open(FILENAME, mode='a', encoding='utf-8') as file:
        file.write("\n--- New Section ---\n")
        file.write("This line is appended.\n")
        file.write("The original content is still safe above.\n")

    print("-> Successfully appended new data.\n")


def write_multiple_lines():
    """
    Demonstrates writing a list of strings using writelines().
    Note: You must include newline characters (\n) yourself.
    """
    print(f"--- 3. Writing a list of lines to {FILENAME} ---")

    lines_of_data = [
        "\n--- List Section ---\n",
        "Item 1: Apples\n",
        "Item 2: Bananas\n",
        "Item 3: Cherries\n"
    ]

    with open(FILENAME, mode='a', encoding='utf-8') as file:
        file.writelines(lines_of_data)

    print("-> Successfully wrote a list of lines.\n")


def safe_creation_mode():
    """
    Demonstrates the 'x' (exclusive creation) mode.
    This is useful when you want to ensure you don't accidentally overwrite an important file.
    It raises a FileExistsError if the file already exists.
    """
    print("--- 4. Safe Creation ('x' mode) ---")

    try:
        # This will fail because we created the file in step 1
        with open(FILENAME, mode='x', encoding='utf-8') as file:
            file.write("This will not be written.")
    except FileExistsError:
        print(f"-> Error caught: '{FILENAME}' already exists. Your data is safe!")
    except Exception as e:
        print(f"-> An unexpected error occurred: {e}")
    print()


def read_verification():
    """
    Helper function to read and print the file content to verify our work.
    """
    print(f"--- Final Verification: Reading {FILENAME} ---")

    if os.path.exists(FILENAME):
        with open(FILENAME, mode='r', encoding='utf-8') as file:
            content = file.read()
            print("File Content Preview:\n")
            print("=" * 30)
            print(content.strip())
            print("=" * 30)
    else:
        print("File not found!")


if __name__ == "__main__":
    # 1. Create/Overwrite file
    write_basic_mode()

    # 2. Add to the file
    append_mode()

    # 3. Add a list of lines
    write_multiple_lines()

    # 4. Try to create it safely (demonstrating error handling)
    safe_creation_mode()

    # 5. Show the result
    read_verification()