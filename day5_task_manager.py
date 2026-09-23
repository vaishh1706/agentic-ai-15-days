
import json
import os

TASK_FILE = "tasks.json"


def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as file:
            return json.load(file)

    return []


def save_tasks(tasks):
    with open(TASK_FILE, "w") as file:
        json.dump(tasks, file, indent=4)


def add_task(tasks):
    task = input("Enter task: ").strip()

    if not task:
        return "Task cannot be empty."

    tasks.append(task)
    save_tasks(tasks)

    return f"Task added: {task}"


def show_tasks(tasks):
    if not tasks:
        return "No tasks available."

    return "\n".join(
        f"{number}. {task}"
        for number, task in enumerate(tasks, start=1)
    )


def delete_task(tasks):
    try:
        number = int(input("Enter task number: "))

        if number < 1 or number > len(tasks):
            return "Invalid task number."

        removed_task = tasks.pop(number - 1)
        save_tasks(tasks)

        return f"Task deleted: {removed_task}"

    except ValueError:
        return "Please enter a valid number."


tool_registry = {
    "add": add_task,
    "show": show_tasks,
    "delete": delete_task
}


tasks = load_tasks()

while True:

    print("\n--- Task Manager ---")
    print("1. Add task")
    print("2. Show tasks")
    print("3. Delete task")
    print("4. Exit")

    choice = input("\nChoose an option: ")

    if choice == "1":
        print(tool_registry["add"](tasks))

    elif choice == "2":
        print("\nYour Tasks:")
        print(tool_registry["show"](tasks))

    elif choice == "3":
        print(tool_registry["delete"](tasks))

    elif choice == "4":
        print("Goodbye!")
        break

    else:
        print("Invalid option.")