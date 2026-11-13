import os
import json
from collections.abc import Callable
from product import Product
from supplier import Supplier
from inventory import Inventory
from can_be_shipped import CanBeShipped
from product_factory import ProductFactory, create_product
import math

FILENAME = "inventory.json"

error_log: list[str] = []
failed_entries: int = 0
suppliers: dict[str, Supplier] = {}

menu = [
    {"Choice" : "1", "Description": "Display All Products"},
    {"Choice" : "2", "Description": "Add Product"},
    {"Choice" : "3", "Description": "Update Stock"},
    {"Choice" : "4", "Description": "Search Product"},
    {"Choice" : "5", "Description": "Save Inventory"},
    {"Choice" : "6", "Description": "Remove Product"},
    {"Choice" : "7", "Description": "Exit"}
]

PRODUCT_TYPE_CHOICES = {"1": "physical", "2": "digital"}
SPECIFIC_PROMPTS = {"physical": "Weight (kg): ", "digital": "Download Size (MB): "}

def log_error(message: str) -> None:
    """Print an error, count it, and keep it for saving to the file."""
    global failed_entries
    failed_entries += 1
    error_log.append(message)
    print("Error:", message)

def read_text(prompt: str) -> str:
    return input(prompt).strip()

def read_number(prompt: str, cast: Callable[[str], float]) -> float | None:
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

def get_positive_float(prompt: str) -> float:
    while True:
        raw = read_text(prompt)
        try:
            value = float(raw)
        except ValueError:
            log_error(f"Invalid input '{raw}'. Please enter a valid number, e.g. 12.50")
            continue
        if value <= 0 or not math.isfinite(value):
            log_error(f"Invalid input '{raw}'. Please enter a number greater than zero.")
            continue
        return value

def load_inventory(inventory: Inventory) -> None:
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
        for item in data.get("suppliers", []):
            try:
                supplier = Supplier.from_dict(item)
                suppliers[supplier.supplier_id.lower()] = supplier
            except (KeyError, TypeError, ValueError) as e:
                print(f"Skipped invalid supplier in file: {e}")

        for item in data.get("products", []):
            try:
                inventory.add_product(create_product(item, suppliers))
            except (KeyError, TypeError, ValueError) as e:
                print(f"Skipped invalid product in file: {e}")      
        print("Inventory loaded successfully.")
    except (json.JSONDecodeError, AttributeError):
        print(f"{FILENAME} is unreadable. Starting with an empty inventory.")

def save_inventory(inventory: Inventory) -> None:
    data = {
        "suppliers": [s.to_dict() for s in suppliers.values()],
        "products": inventory.to_list(),
        "total_units": inventory.get_unit_count(),
        "failed_entries": failed_entries,
        "errors": error_log,
    }

    try:
        with open(FILENAME, "w") as f:
            json.dump(data, f, indent=4)
    except OSError as e:
        print(f"Error saving inventory: {e}")
        return
    print("Inventory saved successfully!\n")

def get_or_create_supplier() -> Supplier | None:
    """Reuse an existing Supplier, or create one independently of any Product."""
    sid = read_text("Supplier ID: ")
    if not sid:
        log_error("Supplier ID cannot be empty.")
        return None
    supplier = suppliers.get(sid.lower())
    if supplier:
        return supplier
    name = read_text("New Supplier Name: ")
    email = read_text("Supplier Email: ")
    try:
        supplier = Supplier(sid, name, email)
    except ValueError as e:
        log_error(str(e))
        return None
    suppliers[supplier.supplier_id.lower()] = supplier
    return supplier

def add_product(inventory: Inventory) -> None:
    print("Add New Product")
    pid = read_text("Product ID: ")

    if not pid or inventory.find_product(pid):
        log_error(f"Product ID '{pid}' is empty or already exists.")
        return
    
    name = read_text("Product Name: ")
    if not Product.is_valid_name(name):
        log_error(f"Invalid product name '{name}'.")
        return

    price = get_positive_float("Price: ")
    
    stock = read_number("Stock Quantity: ", int)
    if stock is None:
        return

    supplier = get_or_create_supplier()
    if supplier is None:
        return

    choice = read_text("Product Type (1 = Physical, 2 = Digital): ")
    product_type = PRODUCT_TYPE_CHOICES.get(choice)
    if product_type is None:
        log_error(f"Invalid product type '{choice}'.")
        return
    specific_value = read_number(SPECIFIC_PROMPTS[product_type], float)
    if specific_value is None:
        return
    try:
        product = ProductFactory.create(product_type, pid, name, price, stock, 
                                        supplier, specific_value)
        inventory.add_product(product)
    except ValueError as e:
        log_error(str(e))
        return
    
    print("Product added successfully!")
    product.supplier.display_information()
    print(f"Tax (10%): ${product.calculate_tax():.2f}\n")
    print(product.get_fulfilment_info())
    if isinstance(product, CanBeShipped):
        print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}\n")
    
 
def update_stock(inventory: Inventory) -> None:
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

 
def search_product(inventory: Inventory) -> None:
    print("Search Product")
    term = read_text("Enter Product ID or Name: ").lower()
    matches = inventory.search_product(term)
    if not matches:
        log_error(f"No product found matching '{term}'.")
        return
    inventory.display_products(matches, show_tax=True)

def remove_product(inventory: Inventory) -> None:
    print("Remove Product")
    pid = read_text("Product ID: ")
    try:
        removed = inventory.remove_product(pid)
    except ValueError as e:
        log_error(str(e))
        return
    print(f"'{removed.name}' removed from inventory (the product itself still exists).\n")
 
def show_menu() -> None:
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
            "5": lambda: save_inventory(inventory),
            "6": lambda: remove_product(inventory),
            }

while True:
    choice = read_text("\nEnter option: ")
    if choice == "7":
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