from dotenv import load_dotenv
from google import genai
import os
import json
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
def calculate_sum(a: int, b: int) -> int:
    return a + b
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
    }
]
prompt = "What is 25 + 17? Use the calculate_sum tool."
interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input=prompt,
    tools=tools
)
for step in interaction.steps:
    if step.type == "function_call":
        print("Gemini requested:", step.name)
        print("Arguments:", step.arguments)
        result = calculate_sum(**step.arguments)
        print("Python executed the tool.")
        print("Tool result:", result)
        final_interaction = client.interactions.create(
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
        print("\nGemini's final answer:")
        print(final_interaction.output_text)