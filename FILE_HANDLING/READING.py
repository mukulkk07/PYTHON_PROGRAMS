"""
Python File Reading Toolkit
===========================
This script demonstrates the three main methods to read data from a .txt file.

Key Concepts Covered:
1. read(): Reads the entire file into a single string.
2. readline(): Reads the file one line at a time (best for memory).
3. readlines(): Reads all lines into a python list.
4. Error Handling: Managing 'FileNotFoundError'.
"""

import os


def create_dummy_file(filename):
    """Helper function to create a file for us to read."""
    content = """Line 1: Python is powerful.
Line 2: File handling is essential.
Line 3: Always close your files!
Line 4: The 'with' statement handles closing for you."""

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"--- Setup: Created '{filename}' for testing ---\n")


def read_whole_file(filename):
    """
    Method 1: .read()
    Reads the ENTIRE file content into a single string variable.
    Use this for smaller files.
    """
    print(f"--- 1. Reading whole file '{filename}' ---")

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()

            print("--- Start of File Content ---")
            print(content)
            print("--- End of File Content ---\n")

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.\n")


def read_line_by_line(filename):
    """
    Method 2: Iterating over the file object.
    This is the most MEMORY EFFICIENT way. It reads one line at a time,
    processes it, and discards it from memory. Best for huge files.
    """
    print(f"--- 2. Reading line-by-line (Memory Efficient) ---")

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            line_number = 1
            for line in file:
                # .strip() removes the invisible newline character at the end
                clean_line = line.strip()
                print(f"Processing Line {line_number}: {clean_line}")
                line_number += 1
        print()

    except FileNotFoundError:
        print(f"Error: File not found.\n")


def read_into_list(filename):
    """
    Method 3: .readlines()
    Reads the entire file and stores it as a list of strings.
    Useful if you need to sort lines or access specific lines by index.
    """
    print(f"--- 3. Reading into a list ---")

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines_list = file.readlines()

            print(f"Total lines stored in list: {len(lines_list)}")
            print(f"The 3rd line is: {lines_list[2].strip()}")
        print()

    except FileNotFoundError:
        print(f"Error: File not found.\n")


def read_first_n_chars(filename, n):
    """
    Method 4: Reading specific chunk size.
    Reads only the first 'n' characters.
    """
    print(f"--- 4. Reading first {n} characters ---")

    with open(filename, 'r', encoding='utf-8') as file:
        chunk = file.read(n)
        print(f"Data chunk: '{chunk}'")
    print()


if __name__ == "__main__":
    target_file = "reading_demo.txt"

    # 1. Setup
    create_dummy_file(target_file)

    # 2. Read everything at once
    read_whole_file(target_file)

    # 3. Read loop (Best Practice for large files)
    read_line_by_line(target_file)

    # 4. Read into a list structure
    read_into_list(target_file)

    # 5. Read specific chunk
    read_first_n_chars(target_file, 15)

    # Cleanup (Optional)
    # os.remove(target_file)