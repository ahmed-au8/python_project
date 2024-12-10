import sqlite3
import argparse
import re
import sys

def display_help():
    print("To Do List Manager")
    print("")
    print("Usage: python python-project.py [option] [arguments]")
    print("")
    print("Options: ")
    print("")
    print("-h: Display this help message")
    print("add <task>: Add a new task")
    print("remove <task_id>: Remove a task by its ID")
    print("complete <completed_id>: Mark a task as completed")
    print("list: View all tasks")
    print("")
    print("Example usage: ")
    print("./python-project.py add (Buy groceries)")
    print("./python-project.py remove 2")
    print("./python-project.py complete 3")
    print("./python-project.py list")
    print("")

# Create a connection to a database called database.db
conn = sqlite3.connect('database.db')

# Create a cursor to perform database operations
cursor = conn.cursor()

# Create tasks table if it does not exist
cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (task_id INTEGER PRIMARY KEY AUTOINCREMENT,
              task TEXT, completed BOOLEAN NOT NULL DEFAULT 0)''')

# Function to add a new task 
def add_task(task):
    cursor.execute("INSERT INTO tasks (task, completed) values (?, ?)", (task,0))
    conn.commit()
    # print(f'Task "{task}" added.')


# Function to remove a task by its ID
def remove_task(task_id):
    cursor.execute("DELETE FROM tasks WHERE task_id = ?", (task_id))
    conn.commit()
    # print(f'Task with ID {task_id} removed.')

def complete_task(completed_id):
    cursor.execute("UPDATE tasks SET completed = 1 WHERE task_id = ?",(completed_id))
    conn.commit()
    # print(f'Task with ID {completed_id} marked as completed.')

def display_tasks():
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    return rows
   

#print(display_tasks())

# Setup argument parser
parser = argparse.ArgumentParser(description="To Do List Manager with SQLite")
parser.add_argument('command', choices=['add', 'remove', 'complete', 'list', 'help'])
parser.add_argument('arguments', nargs='?', help="Arguments for the command(task or task ID)")

# Regular expression for validating task names (only alphanumeric and spaces allowed)
task_name_regex = re.compile(r'^[a-zA-Z0-9\s]+$')

# Regular expression for validating task ID (must be an integer)
task_id_regex = re.compile(r'^\d+$')

# Parse command-line arguments
args = parser.parse_args()

# Handle commands
if args.command == 'add':
    if args.arguments:
        # Validate task name using regular expression (optional, only alphanumeric and spaces)
        if task_name_regex.match(args.arguments):
            add_task(args.arguments)
        else:
            print("Error: Task name contains invalid characters. Only alphanumeric characters and spaces are allowed.")
            display_help()
            sys.exit(1)
    else:
        print("Error: You must provide a task to add.")
        display_help()
        sys.exit(1)

elif args.command == 'remove':
    if args.arguments and task_id_regex.match(args.arguments):
        remove_task(int(args.arguments))
    else:
        print("Error: You must provide a valid task ID (integer) to remove.")
        display_help()
        sys.exit(1)

elif args.command == 'complete':
    if args.arguments and task_id_regex.match(args.arguments):
        complete_task(int(args.arguments))
    else:
        print("Error: You must provide a valid task ID (integer) to mark as completed.")
        display_help()
        sys.exit(1)

elif args.command == 'list':
    print(display_tasks())

else:
    display_help()

