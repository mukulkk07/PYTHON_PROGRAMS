import time
import functools
import logging
import random
from typing import Any, Callable, Dict, List

# --- Configuration & Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Mock database for user roles
USER_ROLES = {
    "admin_user": "admin",
    "analyst_user": "analyst",
    "guest_user": "guest"
}

# Global Context (simulating a logged-in session)
CURRENT_USER = None


# --- Decorator 1: Execution Logger ---
def log_execution(func: Callable) -> Callable:
    """
    Logs the start and end of a function execution, including arguments.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)

        logger.info(f"Adding call to stack: {func.__name__}({signature})")

        try:
            result = func(*args, **kwargs)
            logger.info(f"Function {func.__name__} returned: {str(result)[:50]}...")  # Truncate long output
            return result
        except Exception as e:
            logger.error(f"Function {func.__name__} raised exception: {e}")
            raise

    return wrapper


# --- Decorator 2: Performance Timer ---
def measure_time(func: Callable) -> Callable:
    """
    Calculates and prints the execution time of the decorated function.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        logger.info(f"PERFORMANCE: {func.__name__} took {run_time:.4f} seconds")
        return result

    return wrapper


# --- Decorator 3: Role-Based Access Control (Decorator with Arguments) ---
def require_role(allowed_roles: List[str]) -> Callable:
    """
    Enforces that the CURRENT_USER has one of the allowed roles.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not CURRENT_USER:
                raise PermissionError("Authentication required: No user logged in.")

            user_role = USER_ROLES.get(CURRENT_USER)
            if user_role not in allowed_roles:
                raise PermissionError(
                    f"Access Denied: User '{CURRENT_USER}' (Role: {user_role}) "
                    f"does not have required permissions: {allowed_roles}"
                )

            logger.info(f"ACCESS GRANTED: {CURRENT_USER} authorized for {func.__name__}")
            return func(*args, **kwargs)

        return wrapper

    return decorator


# --- Decorator 4: In-Memory Caching (Memoization) ---
def cache_result(func: Callable) -> Callable:
    """
    Caches the result of a function call based on its arguments.
    Useful for expensive computations.
    """
    cache: Dict[str, Any] = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create a unique key based on arguments
        key = str(args) + str(kwargs)

        if key in cache:
            logger.info(f"CACHE HIT: Returning cached result for {func.__name__}")
            return cache[key]

        result = func(*args, **kwargs)
        cache[key] = result
        logger.info(f"CACHE MISS: Storing result for {func.__name__}")
        return result

    return wrapper


# --- Decorator 5: Automatic Retry Logic ---
def retry(max_retries: int = 3, delay: float = 1.0) -> Callable:
    """
    Retries the execution of a function if it fails with a generic Exception.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    logger.warning(f"Attempt {attempts}/{max_retries} failed for {func.__name__}: {e}")
                    if attempts == max_retries:
                        logger.error(f"All {max_retries} attempts failed.")
                        raise
                    time.sleep(delay)

        return wrapper

    return decorator


# --- Decorator 6: Type Validator (Introspection) ---
def validate_input_types(func: Callable) -> Callable:
    """
    Checks that arguments passed to the function match the type hints.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get type hints
        hints = func.__annotations__

        # Check positional args (skipping 'self' if it's a method)
        arg_names = func.__code__.co_varnames[:func.__code__.co_argcount]

        for idx, arg_val in enumerate(args):
            if idx < len(arg_names):
                arg_name = arg_names[idx]
                if arg_name == 'self': continue

                if arg_name in hints:
                    expected_type = hints[arg_name]
                    if not isinstance(arg_val, expected_type):
                        raise TypeError(
                            f"Argument '{arg_name}' must be {expected_type.__name__}, got {type(arg_val).__name__}")

        return func(*args, **kwargs)

    return wrapper


# --- The Core System ---

class DataProcessor:
    """
    A simulated complex system class that utilizes various decorators.
    """

    @log_execution
    @require_role(["admin"])
    def delete_database(self, db_name: str):
        """Critical operation requiring admin privileges."""
        print(f"!!! DELETING DATABASE: {db_name} !!!")
        time.sleep(0.5)
        return "Database Deleted"

    @measure_time
    @cache_result
    @require_role(["admin", "analyst"])
    def compute_heavy_statistics(self, dataset_id: int):
        """Expensive calculation that benefits from caching."""
        print(f"--- Computing statistics for dataset {dataset_id} ---")
        # Simulate heavy work
        time.sleep(1.5)
        return {"mean": 42.5, "variance": 12.1, "id": dataset_id}

    @retry(max_retries=3, delay=0.5)
    @log_execution
    def fetch_external_api(self, url: str):
        """Simulates an unstable network call."""
        print(f"Connecting to {url}...")
        if random.random() < 0.7:  # 70% chance of failure
            raise ConnectionError("Network unstable")
        return "200 OK: Data Received"

    @validate_input_types
    @log_execution
    def process_financial_data(self, amount: float, currency: str):
        """Strictly typed processing function."""
        print(f"Processing {currency} {amount}")
        return f"Processed {amount} {currency}"


# --- Main Execution Simulation ---

def run_simulation():
    print("==================================================")
    print("   STARTING SECURE DATA PROCESSING SIMULATION")
    print("==================================================")

    processor = DataProcessor()
    global CURRENT_USER

    # Scenario 1: Admin performing heavy tasks and critical ops
    print("\n\n--- SCENARIO 1: ADMIN USER ---")
    CURRENT_USER = "admin_user"

    # First call - should calculate (slow)
    processor.compute_heavy_statistics(101)

    # Second call - should use cache (fast)
    processor.compute_heavy_statistics(101)

    # Admin deletion
    processor.delete_database("production_db")

    # Scenario 2: Analyst trying restricted access
    print("\n\n--- SCENARIO 2: ANALYST USER ---")
    CURRENT_USER = "analyst_user"

    try:
        # Analyst can compute stats
        processor.compute_heavy_statistics(202)
        # Analyst cannot delete DB
        processor.delete_database("production_db")
    except PermissionError as e:
        print(f"Expected Error Caught: {e}")

    # Scenario 3: Unstable Network (Retry Logic)
    print("\n\n--- SCENARIO 3: UNSTABLE NETWORK ---")
    try:
        processor.fetch_external_api("http://api.data-provider.com")
    except Exception:
        print("Final failure after retries.")

    # Scenario 4: Type Validation
    print("\n\n--- SCENARIO 4: TYPE VALIDATION ---")
    try:
        # Passing an int instead of float, and int instead of str
        # Note: In strict Python validation, int is often accepted as float,
        # but our decorator logic is strict.
        processor.process_financial_data(100.50, 500)
    except TypeError as e:
        print(f"Validation Error Caught: {e}")

    print("\n==================================================")
    print("             SIMULATION COMPLETE")
    print("==================================================")


if __name__ == "__main__":
    run_simulation()