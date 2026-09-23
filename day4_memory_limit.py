
# Day 4 - Memory Window Function

conversation_memory = [
    {"role": "user", "message": "My name is Vaishnavi."},
    {"role": "assistant", "message": "Nice to meet you!"},
    {"role": "user", "message": "I am learning Python."},
    {"role": "assistant", "message": "That's great!"},
    {"role": "user", "message": "I am learning Agentic AI."},
    {"role": "assistant", "message": "Keep practicing!"},
    {"role": "user", "message": "Explain RAG."},
    {"role": "assistant", "message": "RAG retrieves information before answering."}
]


def get_recent_memory(memory, limit):
    return memory[-limit:]


recent_messages = get_recent_memory(
    conversation_memory,
    4
)


print("Recent Memory:\n")

for message in recent_messages:
    print(message["role"], ":", message["message"])

print("\nTotal messages:", len(conversation_memory))
print("Recent messages:", len(recent_messages))