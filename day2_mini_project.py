from dotenv import load_dotenv
from google import genai
import os
import json
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
# -----------------------------
# Tools
# -----------------------------
def calculate_sum(a: int, b: int) -> int:
    return a + b
def calculate_multiply(a: int, b: int) -> int:
    return a * b
# -----------------------------
# Tool Registry
# -----------------------------
tool_registry = {
    "calculate_sum": calculate_sum,
    "calculate_multiply": calculate_multiply
}
# -----------------------------
# Tool Declarations
# -----------------------------
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
# -----------------------------
# User Goal
# -----------------------------
user_input = input("\nWhat do you want the agent to calculate?\n> ")
# -----------------------------
# Start Agent
# -----------------------------
interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input=user_input,
    tools=tools
)
# -----------------------------
# Agent Loop
# -----------------------------
while True:
    tool_called = False
    for step in interaction.steps:
        if step.type == "function_call":
            tool_called = True
            print("\n[Agent] Selected tool:", step.name)
            print("[Agent] Arguments:", step.arguments)
            tool_function = tool_registry[step.name]
            result = tool_function(**step.arguments)
            print("[Python] Tool executed.")
            print("[Python] Result:", result)
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
        print("\n[Agent] Final answer:")
        print(interaction.output_text)
        break