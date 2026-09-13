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
tools = [
    {
        "type": "function",
        "name": "calculate_sum",
        "description": "Adds two numbers together.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "integer",
                    "description": "The first number."
                },
                "b": {
                    "type": "integer",
                    "description": "The second number."
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
                    "type": "integer",
                    "description": "The first number."
                },
                "b": {
                    "type": "integer",
                    "description": "The second number."
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
            if step.name == "calculate_sum":
                result = calculate_sum(**step.arguments)
            elif step.name == "calculate_multiply":
                result = calculate_multiply(**step.arguments)
            else:
                result = "Unknown tool"
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