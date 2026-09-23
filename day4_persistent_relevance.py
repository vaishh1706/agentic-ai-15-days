
# Day 4 - Persistent Memory Relevance

import json
import os

MEMORY_FILE = "important_memory.json"


def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)

    return {}


def find_relevant_memory(memory, keyword):
    results = {}

    for key, value in memory.items():
        if (
            keyword.lower() in key.lower()
            or keyword.lower() in str(value).lower()
        ):
            results[key] = value

    return results


important_memory = load_memory()

keyword = input("Search saved memory: ")

results = find_relevant_memory(
    important_memory,
    keyword
)

if results:
    print("\nRelevant Memory:")

    for key, value in results.items():
        print(key, ":", value)

else:
    print("\nNo relevant memory found.")