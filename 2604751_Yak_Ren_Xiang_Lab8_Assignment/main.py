import os
import json

from product import Product
from inventory import Inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from product_factory import create_product

FILENAME = "inventory.json"

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
        
def load_inventory(inventory):
    global error_log, failed_entries
    if not os.path.exists(FILENAME):
        print(f"{FILENAME} not found. Creating a new one.")
        save_inventory(inventory)
        return

    print(f"{FILENAME} found.")
    try:
        with open(FILENAME, "r") as f:
            data = json.load(f)
        error_log = data.get("errors", [])
        failed_entries = data.get("failed_entries", 0)
        for item in data.get("products", []):
            try:
                inventory.add_product(create_product(item))
            except (KeyError, TypeError, ValueError) as e:
                print(f"Skipped invalid product in file: {e}")      
        print("Inventory loaded successfully.")
    except (json.JSONDecodeError, AttributeError):
        print(f"{FILENAME} is unreadable. Starting with an empty inventory.")

def save_inventory(inventory):
    data = {
        "products": inventory.to_list(),
        "total_units": inventory.get_unit_count(),
        "failed_entries": failed_entries,
        "errors": error_log,
    }
    with open(FILENAME, "w") as f:
        json.dump(data, f, indent=4)
    print("Inventory saved successfully!\n")
 
def add_product(inventory):
    print("Add New Product")
    pid = read_text("Product ID: ")

    if not pid or inventory.find_product(pid):
        log_error(f"Product ID '{pid}' is empty or already exists.")
        return
    
    name = read_text("Product Name: ")
    if not Product.is_valid_name(name):
        log_error(f"Invalid product name '{name}'.")
        return
    
    price = read_number("Price: ", float)
    if price is None:
        return
    
    stock = read_number("Stock Quantity: ", int)
    if stock is None:
        return
    
    product_type = read_text("Product Type (1 = Physical, 2 = Digital): ")
    try:
        if product_type == "1":
            weight = read_number("Weight (kg): ", float)
            if weight is None:
                return
            product = PhysicalProduct(pid, name, price, stock, weight)
        elif product_type == "2":
            size = read_number("Download Size (MB): ", float)
            if size is None:
                return
            product = DigitalProduct(pid, name, price, stock, size)
        else:
            log_error(f"Invalid product type '{product_type}'.")
            return
        inventory.add_product(product)
    except ValueError as e:
        log_error(str(e))
        return
    
    print("Product added successfully!")
    print(f"Tax (10%): ${product.calculate_tax():.2f}\n")
    print(product.get_fulfilment_info())
    if isinstance(product, CanBeShipped):
        print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}\n")
    
 
def update_stock(inventory):
    print("Update Stock")
    pid = read_text("Product ID: ")
    product = inventory.find_product(pid)
    if not product:
        log_error(f"Product ID '{pid}' not found.")
        return
    stock = read_number("New Stock Quantity: ", int)
    if stock is None:
        return
    try:
        inventory.update_stock(pid, stock)
    except ValueError as e:
        log_error(str(e))
        return
    print("Stock updated successfully!\n")

 
def search_product(inventory):
    print("Search Product")
    term = read_text("Enter Product ID or Name: ").lower()
    matches = inventory.search_product(term)
    if not matches:
        log_error(f"No product found matching '{term}'.")
        return
    inventory.display_products(matches, show_tax=True)
 
 
def show_menu():
    print("----------- MENU -----------")
    for item in menu:
        print(f"{item['Choice']}. {item['Description']}")
    print("----------------------------")


print("=" * 40)
print("INVENTORY MANAGEMENT SYSTEM")
print("=" * 40)
inventory = Inventory()
load_inventory(inventory)
show_menu()

actions = {
            "1": inventory.display_all, 
            "2": lambda: add_product(inventory), 
            "3": lambda: update_stock(inventory),
            "4": lambda: search_product(inventory), 
            "5": lambda: save_inventory(inventory)
            }

while True:
    choice = read_text("\nEnter option: ")
    if choice == "6":
        break
    if choice in actions:
        actions[choice]()
    else:
        log_error(f"Invalid menu option '{choice}'.\n")

print("\nFinal Summary:")
print("Total Units in Stock:", inventory.get_unit_count())
print("Number of Failed/Rejected Entries:", failed_entries)

if inventory.is_overstocked():
    print("Overstock Alert: Inventory limit reached.")
    
save_inventory(inventory)

print("\nSaving inventory before exit...")
print("Inventory saved successfully.")
print("\nThank you for using Inventory Management System.")
print("Program terminated.")
