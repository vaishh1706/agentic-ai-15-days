from dotenv import load_dotenv
from google import genai
import os
import json

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

prompt = """
Give information about RAG.
"""

response_schema = {
    "type": "object",
    "properties": {
        "topic": {
            "type": "string"
        },
        "difficulty": {
            "type": "string"
        },
        "description": {
            "type": "string"
        }
    },
    "required": [
        "topic",
        "difficulty",
        "description"
    ]
}

interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input=prompt,
    response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": response_schema
    }
)

data = json.loads(interaction.output_text)

print("Topic:", data["topic"])
print("Difficulty:", data["difficulty"])
print("Description:", data["description"])