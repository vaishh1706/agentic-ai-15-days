
from dotenv import load_dotenv
from google import genai
import os
import json

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

user_goal = input("What do you want me to calculate? ")

response_schema = {
    "type": "object",
    "properties": {
        "goal": {"type": "string"},
        "steps": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["add", "multiply"]
                    },
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["operation", "a", "b"]
            }
        }
    },
    "required": ["goal", "steps"]
}

print("\nCreating plan with Gemini...")

try:
    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=f"""
Create a calculation plan for this goal:

{user_goal}

Rules:
- Use only add and multiply.
- Return only JSON matching the schema.
""",
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": response_schema
        }
    )

    plan_data = json.loads(interaction.output_text)

    # Validate the plan
    if not plan_data.get("steps"):
        raise ValueError("The plan is empty.")

    allowed_operations = {"add", "multiply"}

    for step in plan_data["steps"]:
        if step["operation"] not in allowed_operations:
            raise ValueError("Invalid operation.")

    print("\nGemini's Plan:")

    for number, step in enumerate(plan_data["steps"], start=1):
        print(
            f"Step {number}: "
            f"{step['operation']} "
            f"{step['a']} and {step['b']}"
        )

    # Execute the plan
    print("\nExecuting Plan:")

    result = None

    for number, step in enumerate(plan_data["steps"], start=1):

        operation = step["operation"]
        b = step["b"]

        if number == 1:
            a = step["a"]
        else:
            a = result

        if operation == "add":
            result = a + b

        elif operation == "multiply":
            result = a * b

        print(f"Step {number} Result:", result)

    print("\nFinal Answer:", result)

except Exception as error:
    print("\nSomething went wrong.")
    print("Error:", error)
    