from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from product_factory import create_product

try:
    Product("P0", "Generic", 1.0, 1)
except TypeError as e:
    print("Product is abstract:", e)

guitar = PhysicalProduct("P1", "Guitar", 200.0, 3, 4.5)
light = PhysicalProduct("P2", "Book", 20.0, 3, 0.5)
game = DigitalProduct("D1", "Game", 59.9, 10, 2048)

for p in (guitar, game):
    p.display_information(show_tax=True)
    print(p.get_fulfilment_info())

print(guitar.calculate_shipping_cost(), light.calculate_shipping_cost())
print("Digital shippable?", isinstance(game, CanBeShipped))   # False

clone = create_product(guitar.to_dict())
print(type(clone).__name__, clone.weight)                     # round-trip check