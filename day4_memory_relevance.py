
# Day 4 - Memory Relevance Filter

important_memory = {
    "name": "Vaishnavi",
    "goal": "Become an AI engineer",
    "favorite_food": "Pizza",
    "language": "Python"
}


def find_relevant_memory(keyword):
    relevant_memory = {}

    for key, value in important_memory.items():

        if (
            keyword.lower() in key.lower()
            or keyword.lower() in str(value).lower()
        ):
            relevant_memory[key] = value

    return relevant_memory


keyword = input("What information do you need? ")

results = find_relevant_memory(keyword)

if results:
    print("\nRelevant Memory:")

    for key, value in results.items():
        print(key, ":", value)

else:
    print("\nNo relevant memory found.")