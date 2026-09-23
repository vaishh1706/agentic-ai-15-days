
from dotenv import load_dotenv
from google import genai
import os
import json

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

tasks = []


def add_task(task):
    tasks.append(task)
    return f"Task added: {task}"


def show_tasks():
    if not tasks:
        return "No tasks available."

    return "\n".join(
        f"{number}. {task}"
        for number, task in enumerate(tasks, start=1)
    )


def delete_task(task_number):
    if task_number < 1 or task_number > len(tasks):
        return "Invalid task number."

    removed_task = tasks.pop(task_number - 1)
    return f"Task deleted: {removed_task}"


tool_registry = {
    "add_task": add_task,
    "show_tasks": show_tasks,
    "delete_task": delete_task
}


tools = [
    {
        "type": "function",
        "name": "add_task",
        "description": "Adds a new task.",
        "parameters": {
            "type": "object",
            "properties": {
                "task": {"type": "string"}
            },
            "required": ["task"]
        }
    },
    {
        "type": "function",
        "name": "show_tasks",
        "description": "Shows all tasks.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "type": "function",
        "name": "delete_task",
        "description": "Deletes a task using its number.",
        "parameters": {
            "type": "object",
            "properties": {
                "task_number": {"type": "integer"}
            },
            "required": ["task_number"]
        }
    }
]


user_input = input("You: ")

interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input=user_input,
    tools=tools
)


while True:

    tool_called = False

    for step in interaction.steps:

        if step.type == "function_call":

            tool_called = True

            print("\nSelected tool:", step.name)
            print("Arguments:", step.arguments)

            tool_function = tool_registry.get(step.name)

            if tool_function is None:
                print("Unknown tool.")
                break

            result = tool_function(**step.arguments)

            print("Tool result:", result)

            interaction = client.interactions.create(
                model="gemini-3.6-flash",
                previous_interaction_id=interaction.id,
                input=[
                    {
                        "type": "function_result",
                        "name": step.name,
                        "call_id": step.id,
                        "result": [
                            {
                                "type": "text",
                                "text": json.dumps(result)
                            }
                        ]
                    }
                ],
                tools=tools
            )

            break

    if not tool_called:
        print("\nGemini:", interaction.output_text)
        break