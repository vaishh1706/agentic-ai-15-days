
# Day 4 - Memory Mini-Project

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
def save_memory(memory):
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)
def get_context(conversation):
    context = ""
    for message in conversation:
        context += f"{message['role']}: {message['message']}\n"
    return context
important_memory = load_memory()
conversation_memory = []
print("Gemini Memory Agent")
print("Type 'exit' to stop.\n")
while True:
    user_message = input("You: ")
    if user_message.lower() == "exit":
        print("Goodbye!")
        break
    conversation_memory.append({
        "role": "user",
        "message": user_message
    })
    prompt = f"""
You are a helpful AI assistant.
Saved important memory:
{json.dumps(important_memory, indent=2)}
Recent conversation:
{get_context(conversation_memory)}
Answer the user's latest message.
Keep your answer short and clear.
"""
    try:
        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt
        )
        assistant_response = interaction.output_text
        conversation_memory.append({
            "role": "assistant",
            "message": assistant_response
        })
        print("\nGemini:", assistant_response)
        print()
    except Exception as error:
        print("\nSomething went wrong.")
        print("Error:", error)