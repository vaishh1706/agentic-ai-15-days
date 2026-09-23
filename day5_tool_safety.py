
# Day 5 - Safe Tool Execution

tasks = [
    "Learn Python",
    "Study Agentic AI",
    "Practice RAG"
]


def delete_task(task_number):

    if not isinstance(task_number, int):
        return "Task number must be an integer."

    if task_number < 1 or task_number > len(tasks):
        return "Invalid task number."

    removed_task = tasks.pop(task_number - 1)

    return f"Deleted: {removed_task}"


print("Available Tasks:")

for number, task in enumerate(tasks, start=1):
    print(number, ".", task)

try:
    number = int(input("\nEnter task number to delete: "))

    result = delete_task(number)

    print("\nResult:", result)

except ValueError:
    print("\nPlease enter a valid number.")

print("\nRemaining Tasks:")

for number, task in enumerate(tasks, start=1):
    print(number, ".", task)