from dotenv import load_dotenv
from google import genai
import os
import json

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def calculate_sum(a: int, b: int) -> int:
    return a + b


def calculate_multiply(a: int, b: int) -> int:
    return a * b


tool_registry = {
    "calculate_sum": calculate_sum,
    "calculate_multiply": calculate_multiply
}


tools = [
    {
        "type": "function",
        "name": "calculate_sum",
        "description": "Adds two numbers together.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "integer"
                },
                "b": {
                    "type": "integer"
                }
            },
            "required": ["a", "b"]
        }
    },
    {
        "type": "function",
        "name": "calculate_multiply",
        "description": "Multiplies two numbers together.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "integer"
                },
                "b": {
                    "type": "integer"
                }
            },
            "required": ["a", "b"]
        }
    }
]


user_input = input("What do you want me to calculate? ")

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

            print("\nGemini selected:", step.name)
            print("Arguments:", step.arguments)

            tool_function = tool_registry[step.name]

            result = tool_function(**step.arguments)

            print("Python executed the tool.")
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

        print("\nGemini's final answer:")
        print(interaction.output_text)

        break