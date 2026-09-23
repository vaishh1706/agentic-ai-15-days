
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

conversation_memory = []


def add_message(role, message):
    conversation_memory.append({
        "role": role,
        "message": message
    })


def get_context():
    context = ""

    for message in conversation_memory:
        context += f"{message['role']}: {message['message']}\n"

    return context


print("Gemini Memory Chatbot")
print("Type 'exit' to stop.\n")


while True:

    user_message = input("You: ")

    if user_message.lower() == "exit":
        print("Goodbye!")
        break

    add_message("user", user_message)

    prompt = f"""
You are a helpful AI assistant.

Here is the conversation history:
{get_context()}

Respond to the user's latest message.
Keep your answer short and clear.
"""

    try:
        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt
        )

        assistant_response = interaction.output_text

        add_message("assistant", assistant_response)

        print("\nGemini:", assistant_response)
        print()

    except Exception as error:
        print("\nSomething went wrong.")
        print("Error:", error)