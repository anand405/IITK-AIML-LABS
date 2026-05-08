# 💰 Personal Expense Tracker

A production-ready, menu-driven CLI application built in Python to help individuals log daily expenses, categorize spending, track monthly budgets, and persist data across sessions.

---

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Menu Options](#menu-options)
- [Input Validation](#input-validation)
- [Data Persistence](#data-persistence)
- [Logging](#logging)
- [Bug Fixes & Improvements](#bug-fixes--improvements)
- [Sample Output](#sample-output)

---

## ✨ Features

- ➕ Add expenses with date, category, amount, and description
- 📋 View all expenses in a formatted table with totals
- 📊 Track spending against a monthly budget with category-wise breakdown
- 💾 Save and load expenses from a CSV file automatically
- ✅ Full input validation on all fields
- 📝 Logging to both terminal and `expense_tracker.log`
- 🗂️ Supports 7 built-in categories + custom categories
- 🔢 CLI argument support to specify custom CSV file path

---

## 📁 Project Structure

```
personal-expense-tracker/
│
├── personal_expense_tracker.py   # Main application file
├── expenses.csv                  # Auto-generated data file (after first save)
├── expense_tracker.log           # Auto-generated log file
└── README.md                     # Project documentation
```

---

## ⚙️ Requirements

- Python 3.10 or higher
- No external libraries required (uses only Python standard library)

---

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/personal-expense-tracker.git](https://github.com/anand405/IITK-AIML-LABS.git)
   cd personal-expenses-tracker
   ```

2. **Verify Python version:**
   ```bash
   python3 --version
   # Should be 3.10 or higher
   ```

3. **Run the application:**
   ```bash
   python3 personal_expenses.py
   ```

4. **Optional – use a custom CSV file:**
   ```bash
   python3 personal_expenses.py --file my_expenses.csv
   ```

---

## 🖥️ Usage

On startup, the application will:
1. Load any previously saved expenses from the CSV file
2. Prompt you to set a monthly budget
3. Display the interactive menu

```
Welcome to Personal Expense Tracker!
Loaded 3 expense(s) from 'expenses.csv'.

--- Set Monthly Budget ---
Enter your monthly budget: 10000
  Monthly budget set to 10000.00

================================
    Personal Expense Tracker
================================
  1. Add Expense
  2. View Expenses
  3. Track Budget
  4. Save Expenses
  5. Exit
================================
Enter your choice (1-5):
```

---

## 📌 Menu Options

| Option | Action | Description |
|--------|--------|-------------|
| 1 | Add Expense | Log a new expense with date, category, amount, and description |
| 2 | View Expenses | Display all recorded expenses in a formatted table |
| 3 | Track Budget | Compare total spending against monthly budget |
| 4 | Save Expenses | Manually save all expenses to the CSV file |
| 5 | Exit | Auto-saves all expenses and exits the program |

---

## 🛡️ Input Validation

| Field | Validation Rules |
|-------|-----------------|
| Date | Must follow `YYYY-MM-DD` format and be a real calendar date |
| Category | Number must be between 1–7; out-of-range numbers are rejected |
| Amount | Must be a positive number greater than zero |
| Description | Cannot be empty or blank whitespace |

---

## 💾 Data Persistence

- Expenses are saved to `expenses.csv` (or a custom file via `--file` flag)
- The file is **automatically loaded** when the program starts
- The file is **automatically saved** when you choose option 5 (Exit)
- CSV format:

```
Date,Category,Amount,Description
2026-05-08,Food,1000.0,Lunch
2026-05-07,Travel,5000.0,Weekend trip
```

---

## 📝 Logging

All key events are logged to both the **terminal** and **`expense_tracker.log`**:

```
2026-05-08 10:00:01 [INFO] Loaded 3 expense(s) from 'expenses.csv'.
2026-05-08 10:01:22 [INFO] Expense added: {'date': '2026-05-08', ...}
2026-05-08 10:05:10 [WARNING] Budget exceeded by 500.00
2026-05-08 10:10:00 [INFO] Saved 4 expense(s) to 'expenses.csv'.
2026-05-08 10:10:00 [INFO] Application exited by user.
```

---

## 🐛 Bug Fixes & Improvements

The following improvements were made over the base solution:

| # | Issue | Fix Applied |
|---|-------|-------------|
| 1 | Entering category number `8` (out of range) was silently accepted as a custom category `"8"` | Added explicit out-of-range number check — only numbers 1–7 are valid; anything else re-prompts |
| 2 | Budget was set lazily (only when option 3 was visited) | Budget is now set at startup before the menu appears |
| 3 | No validation on date, amount, or empty fields | Full input validation added with helpful error messages |
| 4 | No logging | Logging added to terminal + log file for all key events |
| 5 | Raw `open()` file handling | Replaced with `pathlib.Path` for safer cross-platform file access |

---

## 📸 Sample Output

**Adding an Expense:**
```
--- Add Expense ---
Enter the date (YYYY-MM-DD): 2026-05-08
  Available categories: 1.Food, 2.Travel, 3.Housing, 4.Health, 5.Entertainment, 6.Shopping, 7.Other
  Enter category (e.g., Food, Travel): 1
Enter the amount: 500
Enter a brief description: Grocery shopping
Expense added successfully.
```

**Viewing Expenses:**
```
--- View Expenses ---

  #    Date         Category            Amount  Description
  ────────────────────────────────────────────────────────────────────
  1    2026-05-08   Food               500.00   Grocery shopping
  2    2026-05-07   Travel            5000.00   Weekend trip
  ────────────────────────────────────────────────────────────────────
  TOTAL                               5500.00

  2 valid record(s) displayed.
```

**Tracking Budget:**
```
--- Track Budget ---

  Monthly Budget : 10000.00
  Total Expenses : 5500.00

  You are within your budget. You have 4500.00 remaining.

  Spending by Category:
    Travel            5000.00  ████████████████████
    Food               500.00  ██
```
