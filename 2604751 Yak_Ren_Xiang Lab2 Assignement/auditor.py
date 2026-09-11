Inventory = 0
userinput = ""
FalseEntryCount = 0

while userinput != "quit" and Inventory <= 500:
    userinput = input("Enter Stock Units: ")
    if userinput != "quit" and Inventory <= 500:
        if userinput.isdigit():
            Inventory = Inventory + int(userinput)
            print("Current Inventory:", Inventory, "units")
        else:
            print("Invalid Input. Please enter a number.")
            FalseEntryCount = FalseEntryCount + 1

if userinput == "quit":
    print("Total Units Processed:", Inventory, "units")
    print("Number of Failed/Rejected Entries:", FalseEntryCount)

if Inventory > 500:
    print("Overstock Alert: Inventory limit reached.")