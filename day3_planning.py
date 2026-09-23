# Day 3 - Dynamic Planning
print("Simple Planning Agent")
first_number = int(input("Enter the first number: "))
second_number = int(input("Enter the second number: "))
operation = input("Choose operation (add/multiply): ").lower()
# Create a plan dynamically
if operation == "add":
    plan = f"Add {first_number} and {second_number}"
elif operation == "multiply":
    plan = f"Multiply {first_number} by {second_number}"
else:
    plan = "Invalid operation"
print("\nAgent Plan:", plan)
# Execute the plan
if operation == "add":
    result = first_number + second_number
    print("Executing addition...")
elif operation == "multiply":
    result = first_number * second_number
    print("Executing multiplication...")
else:
    result = None
    print("Unknown operation.")
if result is not None:
    print("Final Answer:", result)