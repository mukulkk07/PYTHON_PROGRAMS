"""
Python Multithreading Demo
==========================
This script demonstrates how to run multiple tasks concurrently using threads.

Key Concepts:
1. threading.Thread: Creating a worker.
2. start(): Begins the thread's activity.
3. join(): Waits for the thread to finish before moving on.
4. I/O Bound tasks: Threads are best for waiting tasks (like downloading files or sleeping).
"""

import threading
import time


def slow_task(task_name, delay):
    """
    A function that simulates a slow task (like downloading a file).
    It simply waits (sleeps) for 'delay' seconds.
    """
    print(f"🟢 [Start] {task_name} (will take {delay}s)")
    time.sleep(delay)
    print(f"🔴 [Done ] {task_name}")


def run_sequentially():
    """
    Runs tasks one after another.
    This is how normal programs work (Single-threaded).
    """
    print("\n--- 1. Sequential Execution (One by One) ---")
    start_time = time.time()

    # We run the task twice. The second one waits for the first to finish.
    slow_task("Task A", 2)
    slow_task("Task B", 2)

    end_time = time.time()
    print(f"⏱️  Total time taken: {end_time - start_time:.2f} seconds")


def run_with_threads():
    """
    Runs tasks at the same time using Multithreading.
    """
    print("\n--- 2. Multithreading Execution (Concurrent) ---")
    start_time = time.time()

    # 1. Create the Thread objects
    # target = the function to run
    # args = the arguments to pass to that function
    t1 = threading.Thread(target=slow_task, args=("Thread-1", 2))
    t2 = threading.Thread(target=slow_task, args=("Thread-2", 2))

    # 2. Start the threads (This launches them in the background)
    t1.start()
    t2.start()

    # At this point, the main program keeps running while t1 and t2 run in background.
    print("   (Main program is waiting for threads to finish...)")

    # 3. Join the threads
    # This tells the main program: "Stop here and wait until t1 and t2 are done."
    t1.join()
    t2.join()

    end_time = time.time()
    print(f"⏱️  Total time taken: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    # Run the slow version
    run_sequentially()

    # Run the fast version
    run_with_threads()