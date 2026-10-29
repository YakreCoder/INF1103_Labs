import os
import json

FILENAME = "inventory.json"
STOCK_LIMIT = 500
TAX_RATE = 0.10

inventory = []
error_log = []
failed_entries = 0

menu = [
    {"Choice" : "1", "Description": "Display All Products"},
    {"Choice" : "2", "Description": "Add Product"},
    {"Choice" : "3", "Description": "Update Stock"},
    {"Choice" : "4", "Description": "Search Product"},
    {"Choice" : "5", "Description": "Save Inventory"},
    {"Choice" : "6", "Description": "Exit"}
]

def log_error(message):
    """Print an error, count it, and keep it for saving to the file."""
    global failed_entries
    failed_entries += 1
    error_log.append(message)
    print("Error:", message)

def get_unit_count():
    return sum(p["stock"] for p in inventory)

def calculate_tax(price, stock):
    return "${:.2f}".format(price * TAX_RATE * stock)

def find_product(product_id):
    for p in inventory:
        if p["id"].lower() == product_id.lower():
            return p
    return None

def read_text(prompt):
    return input(prompt).strip()

def read_number(prompt, cast):
    """Return a non-negative number, or None (and log an error) if invalid."""
    raw = read_text(prompt)
    try:
        value = cast(raw)
        if value < 0:
            raise ValueError
        return value
    except ValueError:
        log_error(f"Invalid input '{raw}' for {prompt.strip(': ')}.")
        return None
 
def format_product(p):
    return f"ID: {p['id']} | Name: {p['name']} | Price: ${p['price']:.2f} | Stock: {p['stock']}"
        
def load_inventory():
    global inventory, error_log, failed_entries
    if os.path.exists(FILENAME):
        print(f"{FILENAME} found.")
        try:
            with open(FILENAME, "r") as f:
                data = json.load(f)
            inventory = data.get("products", [])
            error_log = data.get("errors", [])
            failed_entries = data.get("failed_entries", 0)
            print("Inventory loaded successfully.")
        except (json.JSONDecodeError, AttributeError):
            print(f"{FILENAME} is unreadable. Starting with an empty inventory.")
            inventory = []
    else:
        print(f"{FILENAME} not found. Creating a new one.")
        inventory = []
        error_log = []
        failed_entries = 0
        with open(FILENAME, "w") as f:
            json.dump({"products": [], "total_units": 0,
                       "failed_entries": 0, "errors": []}, f, indent=4)

    
def save_inventory():
    data = {
        "products": inventory,
        "total_units": get_unit_count(),
        "failed_entries": failed_entries,
        "errors": error_log,
    }
    with open(FILENAME, "w") as f:
        json.dump(data, f, indent=4)
    print("Inventory saved successfully!\n")


def display_all():
    print("Current Inventory")
    print("-" * 48)
    if not inventory:
        print("No products in inventory.")
    for p in inventory:
        print(format_product(p))
    print("-" * 48, "\n")

 
def add_product():
    print("Add New Product")
    pid = read_text("Product ID: ")
    if not pid or find_product(pid):
        log_error(f"Product ID '{pid}' is empty or already exists.")
        return
    name = read_text("Product Name: ")
    if not name or name.isdigit():
        log_error(f"Invalid product name '{name}'.")
        return
    price = read_number("Price: ", float)
    if price is None:
        return
    stock = read_number("Stock Quantity: ", int)
    if stock is None:
        return
    if get_unit_count() + stock >= STOCK_LIMIT:
        log_error(f"Overstock Alert: total stock must stay under {STOCK_LIMIT} units.")
        return
    inventory.append({"id": pid, "name": name, "price": price, "stock": stock})
    print("Product added successfully!")
    print("Tax (10%):", calculate_tax(price, stock),"\n")
    
 
def update_stock():
    print("Update Stock")
    pid = read_text("Product ID: ")
    product = find_product(pid)
    if not product:
        log_error(f"Product ID '{pid}' not found.")
        return
    stock = read_number("New Stock Quantity: ", int)
    if stock is None:
        return
    if get_unit_count() - product["stock"] + stock >= STOCK_LIMIT:
        log_error(f"Overstock Alert: total stock must stay under {STOCK_LIMIT} units.")
        return
    product["stock"] = stock

    print("Stock updated successfully!\n")

 
def search_product():
    print("Search Product")
    term = read_text("Enter Product ID or Name: ").lower()
    matches = [p for p in inventory if term in p["id"].lower() or term in p["name"].lower()]
    if not term or not matches:
        log_error(f"No product found matching '{term}'.")
        return
    print("-" * 48)
    for p in matches:
        print(format_product(p), "| Tax:", calculate_tax(p["price"], p["stock"]))
    print("-" * 48, "\n")
 
 
def show_menu():
    print("----------- MENU -----------")
    for item in menu:
        print(f"{item['Choice']}. {item['Description']}")
    print("----------------------------")


print("=" * 40)
print("INVENTORY MANAGEMENT SYSTEM")
print("=" * 40)
load_inventory()
show_menu()

actions = {"1": display_all, "2": add_product, "3": update_stock,
            "4": search_product, "5": save_inventory}

while True:
    choice = read_text("\nEnter option: ")
    if choice == "6":
        break
    if choice in actions:
        actions[choice]()
    else:
        log_error(f"Invalid menu option '{choice}'.\n")

print("\nFinal Summary:")
print("Total Units in Stock:", get_unit_count())
print("Number of Failed/Rejected Entries:", failed_entries)

if get_unit_count() >= STOCK_LIMIT:
    print("Overstock Alert: Inventory limit reached.")
save_inventory()

print("\nSaving inventory before exit...")
print("Inventory saved successfully.")
print("\nThank you for using Inventory Management System.")
print("Program terminated.")
