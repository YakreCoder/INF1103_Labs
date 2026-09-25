inventory = ""
itemname = ""
unitcount = 0
FalseEntryCount = 0
account = ""
index = 0
total_units = 0
import re

def get_unit_input():
    global FalseEntryCount    

    while True:
        unitcount = input("Enter Stock Units (or type 'quit' to exit): ")
        if unitcount == "quit":
            return "quit"
        elif unitcount.isdigit():
            print("Stock Units Accepted:", unitcount)
            return int(unitcount)
        else:
            FalseEntryCount += 1
            print("Invalid Input. Please enter a valid integer or 'quit' to exit.")


def get_itemname_input():
    global FalseEntryCount

    while True:
        itemname = input("Enter Item Name (or type 'quit' to exit): ")
        if itemname == "quit":
            return "quit"
        elif itemname.isdigit():
            FalseEntryCount += 1
            print("Invalid Input. Please enter a valid item or 'quit' to exit.")
        else:
            print("Item Name Accepted:", itemname) 
            return str(itemname)

def get_index_input():
    global FalseEntryCount

    while True:
        index = input("Enter Product ID (or type 'quit' to exit): ")
        if index == "quit":
            return "quit"
        elif index.isdigit():
            print("Product ID Accepted:", index)
            return int(index)
        else:
            FalseEntryCount += 1
            print("Invalid Input. Please enter a valid ID or 'quit' to exit.")
        
# get_valid_input(): Handles the prompt, handles input validation, and
# returns a valid integer or a "quit" signal.

def process_delivery(index,itemname, unitcount):
    inventory = str(index) + ", " + itemname + ", " + str(unitcount)
    return inventory

# process_delivery(current_total, new_value): 
# Calculates the new total and returns it

def get_unit_count(account):
    match = re.search(r'Total Units Processed:\s*(\d+)', account)
    if match:
        return int(match.group(1))
    return 0

def load_inventory():
    try:
        with open("inventory.txt", "r") as file:
            account = str(file.read())
            return account
        
    except FileNotFoundError:
        with open("inventory.txt", "w") as file:
            file.write("Total Units Processed: 0\n")
            file.write("Current Orders:\n")
            file.write("Product ID | Item Name | Quantity\n")

        with open("inventory.txt", "r") as file:
                    account = str(file.read())
                    
        return account
    
def save_inventory(inventory):
    with open("inventory.txt", "a+") as file:
        file.write("\n")
        file.write(str(inventory)) 

def update_units(total_units):
    with open("inventory.txt", "r") as file:
        account = str(file.read())

    with open("inventory.txt", "w") as file:
        account = re.sub(r'Total Units Processed:\s*\d+', f'Total Units Processed: {total_units}', account)
        file.writelines(account)

    return account  

def calculate_tax(unitcount):
    return int(unitcount) * 0.10

# calculate_tax(amount): A new requirement! This function takes a delivery
# amount and returns the tax (10% of that specific delivery)

def generate_report(account,total_units, failed_attempts):
    print(account)
    print("Total Units Processed:", total_units, "units")
    print("Number of Failed/Rejected Entries:", failed_attempts)

# generate_report(total_units, failed_attempts): A dedicated function to print
# the final summary.

account = load_inventory()
print("\nTotal List:\n")
print(account)
total_units = get_unit_count(account)

while total_units <= 500:

    index = get_index_input()
    if index == "quit":
        break

    itemname = get_itemname_input()
    if itemname == "quit":
        break

    unitcount = get_unit_input()
    if unitcount == "quit":
        break

    total_units += int(unitcount)
    
    inventory = process_delivery(index, itemname, unitcount)
    save_inventory(inventory)
    account = update_units(total_units)

    Tax = calculate_tax(unitcount)
    print("Current order:", inventory, "| Delivery Tax:", Tax, "units")

    print("\nTotal list:")
    print(account)

print("\nFinal Summary:")
generate_report(account, total_units, FalseEntryCount)

if total_units > 500:
    print("Overstock Alert: Inventory limit reached.")
