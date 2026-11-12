from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from product_factory import create_product
from supplier import Supplier
from inventory import Inventory
from order import Order

supplier = Supplier("S1", "TechSource", "sales@techsource.com")

try:
    Product("P0", "Generic", 1.0, 1, supplier)  # Should raise an error because Product is abstract
except TypeError as e:
    print("Product is abstract:", e)

guitar = PhysicalProduct("P1", "Guitar", 200.0, 3, supplier, 4.5)
light = PhysicalProduct("P2", "Book", 20.0, 3, supplier, 0.5)
game = DigitalProduct("D1", "Game", 59.9, 10, supplier, 2048)

for p in (guitar, game):
    p.display_information(show_tax=True)
    print(p.get_fulfilment_info())

print(guitar.calculate_shipping_cost(), light.calculate_shipping_cost())
print("Digital shippable?", isinstance(game, CanBeShipped))   # False

clone = create_product(guitar.to_dict(), {supplier.supplier_id.lower(): supplier})
print(type(clone).__name__, clone.weight)                     # round-trip check

def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


print("\n=== Association (Supplier - Product) ===")
guitar.supplier.display_information()
game.supplier.display_information()
print("Same Supplier object shared:", guitar.supplier is game.supplier)
del supplier                                   # PREDICT FIRST
guitar.supplier.display_information()          # still works: the product holds its own reference

print("\n=== Aggregation (Inventory - Product) ===")
inv_a, inv_b = Inventory(), Inventory()
inv_a.add_product(guitar)
removed = inv_a.remove_product("P1")           # PREDICT FIRST
print("Same object returned:", removed is guitar, "| still usable:", removed.name, removed.stock)
inv_b.add_product(removed)
inv_b.add_product(game)
inv_b.add_product(light)
print("A empty:", len(inv_a.products) == 0,
      "| B holds:", [p.product_id for p in inv_b.products])

print("\n=== Composition (Order - OrderLine) ===")
order1, order2 = Order("O1"), Order("O2")
order1.add_order_line(guitar, 1)
order1.add_order_line(game, 2)
order2.add_order_line(guitar, 1)               # PREDICT FIRST
order1.display_information()
print("Same Product in both orders:",
      order1.order_lines[0].product is order2.order_lines[0].product)       # True
print("Different OrderLine objects:",
      order1.order_lines[0] is not order2.order_lines[0])                   # True
order1.remove_order_line("D1")
print("Lines left in O1:", len(order1.order_lines), "| game still exists:", game.name)

print("\n=== LSP + Polymorphism ===")
for product in inv_b.products:                 # PREDICT FIRST: no isinstance, one loop
    show_product_details(product)
    inv_b.update_stock(product.product_id, product.stock + 1)
    print("    stock after update:", product.stock)