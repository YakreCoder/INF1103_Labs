Inventory = 0
userinput = ""
FalseEntryCount = 0

def get_valid_input():
    while True:
        userinput = input("Enter Stock Units (or type 'quit' to exit): ")
        if userinput == "quit":
            return "quit"
        elif userinput.isdigit():
            return int(userinput)
        else:
            print("Invalid Input. Please enter a valid number or 'quit' to exit.")

# get_valid_input(): Handles the prompt, handles input validation, and
# returns a valid integer or a "quit" signal.

def process_delivery(Inventory, userinput):
    return Inventory + int(userinput)

# process_delivery(current_total, new_value): 
# Calculates the new total and returns it

def calculate_tax(userinput):
    return int(userinput) * 0.10

# calculate_tax(amount): A new requirement! This function takes a delivery
# amount and returns the tax (10% of that specific delivery)

def generate_report(total_units, failed_attempts):
    print("Total Units Processed:", total_units, "units")
    print("Number of Failed/Rejected Entries:", failed_attempts)

# generate_report(total_units, failed_attempts): A dedicated function to print
# the final summary.

while Inventory <= 500:
    userinput = get_valid_input()

    if userinput == "quit":
        break
    Inventory = process_delivery(Inventory, userinput)
    FalseEntryCount += 1
    Tax = calculate_tax(userinput)

    print("Current Inventory:", Inventory, "units", "| Delivery Tax:", Tax, "units")

generate_report(Inventory, FalseEntryCount)

if Inventory > 500:
    print("Overstock Alert: Inventory limit reached.")