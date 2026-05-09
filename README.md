# Task Manager with User Authentication

A production-ready, menu-driven CLI application built in Python to manage personal tasks with secure user authentication. Each user can register, log in, and independently manage their own task list. All data is persisted using CSV files.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Menu Options](#menu-options)
- [Input Validation](#input-validation)
- [Data Persistence](#data-persistence)
- [Security](#security)
- [Logging](#logging)
- [Sample Output](#sample-output)


---

## Features

- 🔐 User registration with unique username and hashed password
- 🔑 Secure login with SHA-256 password verification
- ➕ Add tasks with auto-incremented Task IDs
- 📋 View all tasks in a formatted table with status icons
- ✔ Mark tasks as Completed
- 🗑 Delete tasks by Task ID
- 💾 All data saved to CSV files automatically
- 📝 Full logging to terminal and `task_manager.log`
- 👤 Per-user data isolation — no user can access another's tasks

---

## Project Structure

```
task-manager/
│
├── task_manager.py        # Main application file
├── users.csv              # Auto-generated: stores user credentials
├── tasks_<username>.csv   # Auto-generated per user: stores tasks
├── task_manager.log       # Auto-generated: application event log
└── README.md              # Project documentation
```

---

## Requirements

- Python 3.10 or higher
- No external libraries required (uses Python standard library only)

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone    git clone https://github.com/your-username/[task-manager.git](https://github.com/anand405/IITK-AIML-LABS.git)
   git checkout feat/iitk-ml/task-manager
   cd task-manager
   ```

2. **Verify Python version:**
   ```bash
   python3 --version
   # Should be 3.10 or higher
   ```

3. **Run the application:**
   ```bash
   python3 task_manager.py
   ```

---

## Usage

On startup the application shows the main authentication menu:

```
Welcome to Task Manager!
--------------------------------------
1. Register
2. Login
3. Exit
Enter your choice:
```

**First time?** Choose `1` to register, then `2` to log in.

Once logged in, the task management menu appears:

```
======================================
   Task Manager  |  User: alice
======================================
  1. View Tasks
  2. Add Task
  3. Mark Task as Completed
  4. Delete Task
  5. Logout
======================================
Enter your choice:
```

---

## Menu Options

### Authentication Menu

| Option | Action |
|--------|--------|
| 1 | Register a new account |
| 2 | Login to an existing account |
| 3 | Exit the application |

### Task Manager Menu (after login)

| Option | Action |
|--------|--------|
| 1 | View all your tasks |
| 2 | Add a new task |
| 3 | Mark a task as Completed |
| 4 | Delete a task |
| 5 | Logout and return to main menu |

---

## Input Validation

| Field | Rules |
|-------|-------|
| Username | Cannot be empty or contain spaces; must be unique |
| Password | Minimum 6 characters; must be confirmed by re-entry |
| Task description | Cannot be empty or blank whitespace |
| Task ID | Must exist in the task list; enter `0` to cancel any operation |

---

## Data Persistence

### users.csv
Stores all registered user credentials:
```
username,password_hash
alice,5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
bob,6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b
```

### tasks_alice.csv
Stores tasks for user `alice` (one file per user):
```
task_id,description,status
1,Complete Python project,Completed
2,Submit assignment,Pending
3,Review code,Pending
```

- Tasks are saved **immediately** after every add, complete, or delete action
- Each user has their own separate CSV file — data is fully isolated
- Files are created automatically on first use

---

## Security

- **Password hashing** — passwords are hashed with SHA-256 via `hashlib` before storage. Plain-text passwords are never written to disk
- **Secure input** — `getpass.getpass()` is used for all password prompts so characters are not visible on screen
- **Data isolation** — each user's tasks are stored in a separate file (`tasks_<username>.csv`), making cross-user access impossible
- **Failed login logging** — incorrect login attempts are recorded in `task_manager.log` with the username and failure reason

---

## Logging

All key events are logged to both the **terminal** and **`task_manager.log`**:

```
2026-05-09 10:00:01 [INFO] New user registered: 'alice'
2026-05-09 10:01:05 [INFO] User 'alice' logged in.
2026-05-09 10:02:10 [INFO] Task #1 added for 'alice': Complete Python project
2026-05-09 10:03:22 [INFO] Task #1 marked completed for 'alice'.
2026-05-09 10:04:15 [INFO] Task #1 deleted for 'alice'.
2026-05-09 10:05:00 [INFO] User 'alice' logged out.
2026-05-09 10:05:00 [INFO] Application exited.
```

---

## Sample Output

**Adding and viewing tasks:**
```
--- Add Task ---
Enter the task description: Complete Python project
Task added successfully. [Task ID: 1]

--- Your Tasks ---

  Task ID    Status         Description
  ------------------------------------------------------------
  1          ○ Pending      Complete Python project
  2          ✔ Completed    Submit assignment
  ------------------------------------------------------------
  Total: 2  |  Completed: 1  |  Pending: 1
```

**Marking a task as completed:**
```
Enter the Task ID to mark as completed (or 0 to cancel): 1
Task marked as completed: 'Complete Python project'
```

**Deleting a task:**
```
Enter the Task ID to delete (or 0 to cancel): 1
Task deleted successfully: 'Complete Python project'
```
