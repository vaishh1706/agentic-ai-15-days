
# Day 3 - Error Handling

plan = {
    "steps": []
}

try:
    if not plan["steps"]:
        raise ValueError("The plan contains no steps.")

    print("Plan is valid.")

except ValueError as error:
    print("Planning error:", error)