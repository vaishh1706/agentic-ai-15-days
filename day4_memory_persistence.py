
# Day 4 - Persistent Memory + Gemini

from dotenv import load_dotenv
from google import genai
import os
import json

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

MEMORY_FILE = "important_memory.json"


def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)

    return {}


# Load saved memory
important_memory = load_memory()

print("Saved Memory:")
print(important_memory)

user_question = input("\nAsk Gemini something: ")

# Convert memory into context
memory_context = json.dumps(important_memory, indent=2)

prompt = f"""
You are a helpful AI assistant.

Here is the user's saved memory:
{memory_context}

Use the saved memory when relevant.

User's question:
{user_question}

Keep your answer short and clear.
"""

try:
    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )

    print("\nGemini:", interaction.output_text)

except Exception as error:
    print("\nSomething went wrong.")
    print("Error:", error)