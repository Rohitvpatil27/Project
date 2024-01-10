#Project:"Personal Finance Tracker" 
#Simple personal finance tracker that allows users to track their income, expenses, and savings.


import sqlite3
from getpass import getpass
import matplotlib.pyplot as plt
import datetime

# Database initialization
conn = sqlite3.connect('finance_tracker.db')
cursor = conn.cursor()

# Create User table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    monthly_budget REAL
)
''')

# Create Expense table
cursor.execute('''
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    category TEXT,
    amount REAL,
    date DATE,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
''')

# Create Income table
cursor.execute('''
CREATE TABLE IF NOT EXISTS income (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    source TEXT,
    amount REAL,
    date DATE,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
''')

# Create Savings table
cursor.execute('''
CREATE TABLE IF NOT EXISTS savings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    goal TEXT,
    target REAL,
    progress REAL,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
''')

# Create Reminder table
cursor.execute('''
CREATE TABLE IF NOT EXISTS reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    description TEXT,
    date DATE,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
''')

conn.commit()

# User Authentication
def register_user(username, password, monthly_budget):
    cursor.execute('INSERT INTO users (username, password, monthly_budget) VALUES (?, ?, ?)', (username, password, monthly_budget))
    conn.commit()

def login_user(username, password):
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()
    return user

# Expense Tracking
def add_expense(user_id, category, amount):
    date = datetime.datetime.now().date()
    cursor.execute('INSERT INTO expenses (user_id, category, amount, date) VALUES (?, ?, ?, ?)',
                   (user_id, category, amount, date))
    conn.commit()

# Income Tracking
def add_income(user_id, source, amount):
    date = datetime.datetime.now().date()
    cursor.execute('INSERT INTO income (user_id, source, amount, date) VALUES (?, ?, ?, ?)',
                   (user_id, source, amount, date))
    conn.commit()

# Budgeting
def set_monthly_budget(user_id, monthly_budget):
    cursor.execute('UPDATE users SET monthly_budget=? WHERE id=?', (monthly_budget, user_id))
    conn.commit()

def get_monthly_budget(user_id):
    cursor.execute('SELECT monthly_budget FROM users WHERE id=?', (user_id,))
    budget = cursor.fetchone()
    return budget[0] if budget else None

def check_budget_exceed(user_id, category, amount):
    monthly_budget = get_monthly_budget(user_id)

    if monthly_budget is not None:
        cursor.execute('SELECT SUM(amount) FROM expenses WHERE user_id=? AND category=?', (user_id, category))
        category_expenses = cursor.fetchone()[0] or 0

        if category_expenses + amount > monthly_budget:
            return True

    return False

# Visualization
def plot_expense_category_pie(user_id):
    cursor.execute('SELECT category, SUM(amount) FROM expenses WHERE user_id=? GROUP BY category', (user_id,))
    data = cursor.fetchall()

    if not data:
        print("No expenses recorded.")
        return

    categories, amounts = zip(*data)
    plt.pie(amounts, labels=categories, autopct='%1.1f%%')
    plt.title('Expense Distribution')
    plt.show()

# Saving Goals
def add_saving_goal(user_id, goal, target):
    cursor.execute('INSERT INTO savings (user_id, goal, target, progress) VALUES (?, ?, ?, 0)',
                   (user_id, goal, target))
    conn.commit()

def update_saving_progress(user_id, goal_id, progress):
    cursor.execute('UPDATE savings SET progress=? WHERE id=? AND user_id=?', (progress, goal_id, user_id))
    conn.commit()

# Reminder System
def add_reminder(user_id, description, date):
    cursor.execute('INSERT INTO reminders (user_id, description, date) VALUES (?, ?, ?)',
                   (user_id, description, date))
    conn.commit()

# Main Program
if __name__ == '__main__':
    # Example usage of functions
    username = input("Enter username: ")
    password = getpass("Enter password: ")

    user = login_user(username, password)

    if user:
        print("Login successful.")
        user_id = user[0]

        # Example usage of functions
        add_expense(user_id, 'Groceries', 50.0)
        add_expense(user_id, 'Dining Out', 30.0)
        add_income(user_id, 'Salary', 3000.0)
        add_saving_goal(user_id, 'Vacation', 1000.0)
        update_saving_progress(user_id, 1, 500.0)

        monthly_budget = get_monthly_budget(user_id)
        print(f"Monthly Budget: {monthly_budget}")

        set_monthly_budget(user_id, 2000.0)

        if check_budget_exceed(user_id, 'Groceries', 60.0):
            print("Budget Exceeded for Groceries!")

        plot_expense_category_pie(user_id)

        add_reminder(user_id, 'Pay Rent', '2024-02-01')

    else:
        print("Login failed. Invalid credentials.")
