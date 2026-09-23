# Day 4 - Dynamic Important Memory
important_memory = {}
def save_memory(key, value):
    important_memory[key] = value
    print("Memory saved successfully!")
def show_memory():
    print("\nImportant Memory:")
    if not important_memory:
        print("No memories saved.")
        return
    for key, value in important_memory.items():
        print(key, ":", value)
# Save information dynamically
save_memory("name", "Vaishnavi")
save_memory("goal", "Become internship-ready in Agentic AI")
save_memory("language", "Python")
# Display saved information
show_memory()