"""
Python File Detection Toolkit
=============================
This script demonstrates different methods to detect, find, and list files.

Key Concepts Covered:
1. os.path.exists: Check if a specific file is there.
2. os.listdir: List everything in a specific folder.
3. glob: Find files matching a pattern (e.g., *.png).
4. os.walk: Recursively search through all subfolders.
"""

import os
import glob


def check_specific_file(filepath):
    """
    1. Check if a specific file exists.
    """
    print(f"--- 1. Checking for specific file: '{filepath}' ---")

    if os.path.exists(filepath):
        # It exists, but is it actually a file (and not a folder)?
        if os.path.isfile(filepath):
            print(f"✅ STATUS: Found! '{filepath}' exists and is a file.")

            # Optional: Get file size
            size = os.path.getsize(filepath)
            print(f"   Size: {size} bytes")
        else:
            print(f"⚠️ STATUS: '{filepath}' exists, but it is a folder, not a file.")
    else:
        print(f"❌ STATUS: '{filepath}' does not exist.")
    print()


def list_files_in_current_folder():
    """
    2. List all files in the current working directory.
    Ignores folders, lists only files.
    """
    current_dir = os.getcwd()
    print(f"--- 2. Listing files in current folder: {current_dir} ---")

    # Get all entries (files and folders)
    all_entries = os.listdir(current_dir)

    file_count = 0
    for entry in all_entries:
        # Check if it is a file
        if os.path.isfile(entry):
            print(f"   📄 {entry}")
            file_count += 1

    if file_count == 0:
        print("   (No files found in this directory)")
    print()


def find_files_by_extension(extension):
    """
    3. Use glob to find files matching a pattern (e.g., .txt, .py).
    """
    print(f"--- 3. Searching for '*{extension}' files ---")

    # glob.glob returns a list of matching paths
    pattern = f"*{extension}"
    matched_files = glob.glob(pattern)

    if matched_files:
        print(f"Found {len(matched_files)} files matching '{pattern}':")
        for file in matched_files:
            print(f"   🔎 {file}")
    else:
        print(f"   No files found matching '{pattern}'.")
    print()


def deep_scan_directory(start_path):
    """
    4. Recursively walk through the directory tree.
    This looks inside the folder, and inside every sub-folder.
    """
    print(f"--- 4. Deep Scan (Recursive) starting from: {start_path} ---")

    file_count = 0

    # os.walk yields a 3-tuple: (current_folder, sub_folders_list, files_list)
    for root, dirs, files in os.walk(start_path):
        for name in files:
            # Join the root and name to get the full path
            full_path = os.path.join(root, name)
            print(f"   📂 Detected: {full_path}")
            file_count += 1

            # Safety break: Stop if we find too many files (for demo purposes)
            if file_count >= 10:
                print("   ... (Stopping scan after 10 files for brevity) ...")
                return

    if file_count == 0:
        print("   Directory is empty.")
    print()


if __name__ == "__main__":
    # --- Create a dummy file for testing ---
    dummy_name = "test_file.txt"
    with open(dummy_name, "w") as f:
        f.write("I exist!")

    # 1. Check for the dummy file
    check_specific_file(dummy_name)

    # 2. Check for a file that doesn't exist
    check_specific_file("ghost_file.txt")

    # 3. List all files where the script is running
    list_files_in_current_folder()

    # 4. Find all Python files
    find_files_by_extension(".py")

    # 5. Deep scan of the current directory
    deep_scan_directory(".")

    # Cleanup: Remove the dummy file
    # os.remove(dummy_name)