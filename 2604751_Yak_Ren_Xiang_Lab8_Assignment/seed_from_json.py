import json
from product_repository import ProductRepository

with open("inventory.json") as f:
    data = json.load(f)

repo = ProductRepository()
repo.save_products(data["products"])
repo.save_errors(data["errors"])
repo.close()
print(f"Migrated {len(data['products'])} products and {len(data['errors'])} errors.")