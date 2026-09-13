from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

question = input("Ask Gemini something: ")

try:
    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=question
    )

    print("\nGemini:", interaction.output_text)

except Exception as e:
    print("\nSomething went wrong.")
    print("Error:", e)