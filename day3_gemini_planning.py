
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
                        "enum": ["multiply", "add"]
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
- Use only multiply and add operations.
- The first step must contain both original numbers.
- Every later step must use the previous result as a.
- Return only the required JSON structure.
""",
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": response_schema
        }
    )

    plan_data = json.loads(interaction.output_text)

    if not plan_data.get("steps"):
        raise ValueError("The plan contains no steps.")

    allowed_operations = {"add", "multiply"}

    for step in plan_data["steps"]:
        if step.get("operation") not in allowed_operations:
            raise ValueError("Invalid operation.")

        if not isinstance(step.get("a"), (int, float)):
            raise ValueError("Invalid first number.")

        if not isinstance(step.get("b"), (int, float)):
            raise ValueError("Invalid second number.")

    print("\nGoal:", plan_data["goal"])
    print("\nGemini's Plan:")

    for number, step in enumerate(plan_data["steps"], start=1):
        print(
            f"Step {number}: "
            f"{step['operation']} "
            f"{step['a']} and {step['b']}"
        )

    print("\nExecuting Plan:")

    result = None

    for number, step in enumerate(plan_data["steps"], start=1):

        operation = step["operation"]
        b = step["b"]

        # Use Gemini's first number only for the first step.
        # For later steps, use the previous result.
        if number == 1:
            a = step["a"]
        else:
            a = result

        if operation == "multiply":
            result = a * b

        elif operation == "add":
            result = a + b

        print(f"Step {number} Result:", result)

    print("\nFinal Answer:", result)

except Exception as error:
    print("\nSomething went wrong.")
    print("Error type:", type(error).__name__)
    print("Error details:", error)