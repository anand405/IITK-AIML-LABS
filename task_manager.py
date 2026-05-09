"""
task_manager.py
===============
Production-ready Task Manager with User Authentication
Storage : CSV files (users.csv + tasks_<username>.csv)
Author  :Anand Gunda
Version : 1.0.0

Usage:
    python task_manager.py
"""

import csv
import sys
import hashlib
import getpass
import logging
from pathlib import Path

# ── Logging configuration ─────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("task_manager.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# ── Constants ─────────────────────────────────────────────────────────────────
USERS_FILE        = "users.csv"
USERS_HEADERS     = ["username", "password_hash"]
TASKS_HEADERS     = ["task_id", "description", "status"]
STATUS_PENDING    = "Pending"
STATUS_COMPLETED  = "Completed"


# ─────────────────────────────────────────────────────────────────────────────
# UTILITY HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def hash_password(password: str) -> str:
    """Return a SHA-256 hex digest of the given password."""
    return hashlib.sha256(password.encode()).hexdigest()


def tasks_file(username: str) -> Path:
    """Return the Path to the tasks CSV for a specific user."""
    return Path(f"tasks_{username}.csv")


# ─────────────────────────────────────────────────────────────────────────────
# FILE I/O  —  USERS
# ─────────────────────────────────────────────────────────────────────────────
def load_users() -> dict[str, str]:
    """
    Load all registered users from users.csv.

    Returns:
        dict mapping username -> password_hash
    """
    users: dict[str, str] = {}
    filepath = Path(USERS_FILE)
    if not filepath.exists():
        return users
    try:
        with filepath.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if "username" in row and "password_hash" in row:
                    users[row["username"].strip()] = row["password_hash"].strip()
    except (IOError, OSError) as exc:
        logger.error("Failed to load users: %s", exc)
    return users


def save_user(username: str, password_hash: str) -> None:
    """
    Append a new user record to users.csv.
    Creates the file with headers if it does not exist.

    Args:
        username:      New user's username.
        password_hash: SHA-256 hash of the password.
    """
    filepath = Path(USERS_FILE)
    write_header = not filepath.exists()
    try:
        with filepath.open("a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=USERS_HEADERS)
            if write_header:
                writer.writeheader()
            writer.writerow({"username": username,
                             "password_hash": password_hash})
    except (IOError, OSError) as exc:
        logger.error("Failed to save user '%s': %s", username, exc)
        print(f"  [Error] Could not save user: {exc}")


# ─────────────────────────────────────────────────────────────────────────────
# FILE I/O  —  TASKS
# ─────────────────────────────────────────────────────────────────────────────
def load_tasks(username: str) -> list[dict]:
    """
    Load all tasks for a given user from tasks_<username>.csv.

    Args:
        username: The logged-in user's username.

    Returns:
        list of task dicts with keys: task_id, description, status.
    """
    tasks: list[dict] = []
    filepath = tasks_file(username)
    if not filepath.exists():
        return tasks
    try:
        with filepath.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if all(k in row for k in TASKS_HEADERS):
                    tasks.append({
                        "task_id":     row["task_id"].strip(),
                        "description": row["description"].strip(),
                        "status":      row["status"].strip(),
                    })
                else:
                    logger.warning("Skipping malformed row in '%s': %s",
                                   filepath.name, row)
    except (IOError, OSError) as exc:
        logger.error("Failed to load tasks for '%s': %s", username, exc)
    return tasks


def save_tasks(username: str, tasks: list[dict]) -> None:
    """
    Overwrite tasks_<username>.csv with the current in-memory task list.
    CSV quoting handles commas or special characters inside descriptions safely.

    Args:
        username: The logged-in user's username.
        tasks:    List of task dicts to persist.
    """
    try:
        with tasks_file(username).open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=TASKS_HEADERS)
            writer.writeheader()
            writer.writerows(tasks)
        logger.info("Tasks saved for '%s' (%d task(s)).", username, len(tasks))
    except (IOError, OSError) as exc:
        logger.error("Failed to save tasks for '%s': %s", username, exc)
        print(f"  [Error] Could not save tasks: {exc}")


def next_task_id(tasks: list[dict]) -> int:
    """
    Return the next sequential task ID (max existing ID + 1).
    Safe even after deletions — no ID collisions.

    Args:
        tasks: Current in-memory task list.

    Returns:
        Integer ID for the new task.
    """
    ids = []
    for t in tasks:
        try:
            ids.append(int(t["task_id"]))
        except ValueError:
            pass
    return max(ids) + 1 if ids else 1


# ─────────────────────────────────────────────────────────────────────────────
# 1. USER AUTHENTICATION
# ─────────────────────────────────────────────────────────────────────────────
def register() -> None:
    """
    Prompt for a new username and password.
    Validates uniqueness, confirms password, hashes with SHA-256,
    and stores credentials in users.csv.
    """
    print("\n--- Register ---")
    users = load_users()

    # ── Username ──────────────────────────────────────────────────────────────
    while True:
        username = input("Enter a username: ").strip()
        if not username:
            print("  [Error] Username cannot be empty.")
            continue
        if " " in username:
            print("  [Error] Username cannot contain spaces.")
            continue
        if username in users:
            print(f"  [Error] Username '{username}' already exists. Try another.")
            continue
        break

    # ── Password ──────────────────────────────────────────────────────────────
    while True:
        password = getpass.getpass("Enter a password (min 6 characters): ")
        if len(password) < 6:
            print("  [Error] Password must be at least 6 characters.")
            continue
        confirm = getpass.getpass("Confirm your password: ")
        if password != confirm:
            print("  [Error] Passwords do not match. Try again.")
            continue
        break

    # Hash and persist
    hashed_password = hash_password(password)
    save_user(username, hashed_password)

    logger.info("New user registered: '%s'", username)
    print("Registration successful!")


def login() -> tuple[bool, str | None]:
    """
    Prompt for username and password, validate against users.csv.

    Returns:
        (True, username) on success — (False, None) on failure.
    """
    print("\n--- Login ---")

    username = input("Enter your username: ").strip()
    if not username:
        print("  [Error] Username cannot be empty.")
        return False, None

    password = getpass.getpass("Enter your password: ")
    hashed_password = hash_password(password)

    users = load_users()

    if username not in users:
        print("  [Error] Username not found. Please register first.")
        logger.warning("Failed login: unknown user '%s'.", username)
        return False, None

    if users[username] != hashed_password:
        print("  [Error] Incorrect password. Please try again.")
        logger.warning("Failed login: wrong password for user '%s'.", username)
        return False, None

    logger.info("User '%s' logged in.", username)
    print("Login successful!")
    return True, username


# ─────────────────────────────────────────────────────────────────────────────
# 2. ADD A TASK
# ─────────────────────────────────────────────────────────────────────────────
def add_task(username: str) -> None:
    """
    Prompt for a task description, assign the next sequential ID,
    set status to Pending, and save to tasks_<username>.csv.

    Commas inside descriptions are handled safely by csv.DictWriter quoting.

    Args:
        username: The logged-in user's username.
    """
    print("\n--- Add Task ---")

    while True:
        description = input("Enter the task description: ").strip()
        if description:
            break
        print("  [Error] Task description cannot be empty.")

    tasks = load_tasks(username)
    task_id = next_task_id(tasks)

    new_task = {
        "task_id":     str(task_id),
        "description": description,
        "status":      STATUS_PENDING,
    }
    tasks.append(new_task)
    save_tasks(username, tasks)

    logger.info("Task #%d added for '%s': %s", task_id, username, description)
    print(f"Task added successfully. [Task ID: {task_id}]")


# ─────────────────────────────────────────────────────────────────────────────
# 3. VIEW TASKS
# ─────────────────────────────────────────────────────────────────────────────
def view_tasks(username: str) -> None:
    """
    Read tasks_<username>.csv and display all tasks in a formatted table.
    Shows Task ID, status icon, and description for every task.

    Args:
        username: The logged-in user's username.
    """
    print("\n--- Your Tasks ---")
    tasks = load_tasks(username)

    if not tasks:
        print("  No tasks found. Add a task to get started!")
        return

    print(f"\n  {'Task ID':<10} {'Status':<14} Description")
    print("  " + "─" * 60)

    for task in tasks:
        icon = "✔" if task["status"] == STATUS_COMPLETED else "○"
        print(f"  {task['task_id']:<10} {icon} {task['status']:<12} "
              f"{task['description']}")

    completed = sum(1 for t in tasks if t["status"] == STATUS_COMPLETED)
    pending   = len(tasks) - completed
    print("  " + "─" * 60)
    print(f"  Total: {len(tasks)}  |  Completed: {completed}  |  Pending: {pending}")


# ─────────────────────────────────────────────────────────────────────────────
# 4. MARK A TASK AS COMPLETED
# ─────────────────────────────────────────────────────────────────────────────
def mark_task_completed(username: str) -> None:
    """
    Display tasks, prompt for a Task ID, update its status to Completed,
    and rewrite tasks_<username>.csv.

    Args:
        username: The logged-in user's username.
    """
    print("\n--- Mark Task as Completed ---")
    tasks = load_tasks(username)

    if not tasks:
        print("  No tasks available.")
        return

    view_tasks(username)

    if all(t["status"] == STATUS_COMPLETED for t in tasks):
        print("\n  All tasks are already completed!")
        return

    while True:
        task_id = input("\n  Enter the Task ID to mark as completed "
                        "(or 0 to cancel): ").strip()
        if task_id == "0":
            print("  Cancelled.")
            return
        if not task_id:
            print("  [Error] Task ID cannot be empty.")
            continue
        matched = [t for t in tasks if t["task_id"] == task_id]
        if not matched:
            print(f"  [Error] No task found with ID '{task_id}'. Try again.")
            continue
        if matched[0]["status"] == STATUS_COMPLETED:
            print("  [Info] Task is already marked as Completed.")
            return
        break

    for task in tasks:
        if task["task_id"] == task_id:
            task["status"] = STATUS_COMPLETED
            description = task["description"]
            break

    save_tasks(username, tasks)
    logger.info("Task #%s marked completed for '%s'.", task_id, username)
    print(f"Task marked as completed: '{description}'")


# ─────────────────────────────────────────────────────────────────────────────
# 5. DELETE A TASK
# ─────────────────────────────────────────────────────────────────────────────
def delete_task(username: str) -> None:
    """
    Display tasks, prompt for a Task ID, remove it from the list,
    and rewrite tasks_<username>.csv without that entry.

    Args:
        username: The logged-in user's username.
    """
    print("\n--- Delete Task ---")
    tasks = load_tasks(username)

    if not tasks:
        print("  No tasks available.")
        return

    view_tasks(username)

    while True:
        task_id = input("\n  Enter the Task ID to delete "
                        "(or 0 to cancel): ").strip()
        if task_id == "0":
            print("  Cancelled.")
            return
        if not task_id:
            print("  [Error] Task ID cannot be empty.")
            continue
        matched = [t for t in tasks if t["task_id"] == task_id]
        if not matched:
            print(f"  [Error] No task found with ID '{task_id}'. Try again.")
            continue
        break

    description = matched[0]["description"]
    tasks = [t for t in tasks if t["task_id"] != task_id]
    save_tasks(username, tasks)

    logger.info("Task #%s deleted for '%s'.", task_id, username)
    print(f"Task deleted successfully: '{description}'")


# ─────────────────────────────────────────────────────────────────────────────
# 6. INTERACTIVE MENU
# ─────────────────────────────────────────────────────────────────────────────
def task_manager_menu(username: str) -> None:
    """
    Display the task management menu for the authenticated user.
    Loops until the user selects Logout.

    Args:
        username: The authenticated user's username.
    """
    while True:
        print(f"\n{'=' * 38}")
        print(f"   Task Manager  |  User: {username}")
        print(f"{'=' * 38}")
        print("  1. Add Task")
        print("  2. View Tasks")
        print("  3. Mark Task as Completed")
        print("  4. Delete Task")
        print("  5. Logout")
        print(f"{'=' * 38}")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_task(username)
        elif choice == "2":
            view_tasks(username)
        elif choice == "3":
            mark_task_completed(username)
        elif choice == "4":
            delete_task(username)
        elif choice == "5":
            logger.info("User '%s' logged out.", username)
            print("Logging out...")
            break
        else:
            print("  [Error] Invalid choice, please try again.")


def main() -> None:
    """
    Application entry point.
    Shows the outer Register / Login / Exit menu.
    On successful login, enters the task manager menu loop.
    """
    print("\nWelcome to Task Manager!")
    print("─" * 38)

    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            register()
        elif choice == "2":
            logged_in, username = login()
            if logged_in:
                task_manager_menu(username)
        elif choice == "3":
            logger.info("Application exited.")
            print("Exiting the program.")
            break
        else:
            print("  [Error] Invalid choice, please try again.")


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()