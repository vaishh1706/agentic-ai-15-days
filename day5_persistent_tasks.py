
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


def add_task(tasks, task):
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


def delete_task(tasks, task_number):
    if task_number < 1 or task_number > len(tasks):
        return "Invalid task number."

    removed_task = tasks.pop(task_number - 1)
    save_tasks(tasks)

    return f"Task deleted: {removed_task}"


tasks = load_tasks()

print("Task Manager")
print("1. Add task")
print("2. Show tasks")
print("3. Delete task")

choice = input("\nChoose an option: ")

if choice == "1":
    task = input("Enter task: ")
    print(add_task(tasks, task))

elif choice == "2":
    print("\nYour Tasks:")
    print(show_tasks(tasks))

elif choice == "3":
    number = int(input("Enter task number: "))
    print(delete_task(tasks, number))

else:
    print("Invalid option.")