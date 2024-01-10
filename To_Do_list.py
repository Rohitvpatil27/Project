#Project-To_Do_lsit
#Application that allows users to manage and keep track of tasks or activities they need to complete. 


import os

tasks = []

def display_menu():
    print("\nTo-Do List Menu:")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Mark as Complete")
    print("4. Delete Task")
    print("5. Save and Quit")

def add_task():
    task = input("Enter the task: ")
    tasks.append({"task": task, "status": "Incomplete"})
    print("Task added!")

def view_tasks():
    if not tasks:
        print("No tasks found.")
    else:
        print("\nTasks:")
        for index, task in enumerate(tasks, 1):
            print(f"{index}. [{task['status']}] {task['task']}")

def mark_complete():
    view_tasks()
    try:
        task_index = int(input("Enter the task number to mark as complete: ")) - 1
        tasks[task_index]["status"] = "Complete"
        print("Task marked as complete!")
    except (ValueError, IndexError):
        print("Invalid input. Please enter a valid task number.")

def delete_task():
    view_tasks()
    try:
        task_index = int(input("Enter the task number to delete: ")) - 1
        deleted_task = tasks.pop(task_index)
        print(f"Task '{deleted_task['task']}' deleted!")
    except (ValueError, IndexError):
        print("Invalid input. Please enter a valid task number.")

def save_and_quit():
    with open("todolist.txt", "w") as file:
        for task in tasks:
            file.write(f"{task['task']}|{task['status']}\n")
    print("To-Do List saved. Goodbye!")

def load_todo_list():
    if os.path.exists("todolist.txt"):
        with open("todolist.txt", "r") as file:
            for line in file:
                task, status = line.strip().split("|")
                tasks.append({"task": task, "status": status})

def main():
    load_todo_list()

    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            mark_complete()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            save_and_quit()
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()

