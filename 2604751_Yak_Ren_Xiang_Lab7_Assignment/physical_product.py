from can_be_shipped import CanBeShipped
from product import Product

class PhysicalProduct(Product, CanBeShipped):
    """A product that is shipped to the customer."""

    BASE_SHIPPING_FEE = 5.00
    COST_PER_KG = 2.00

    def __init__(self, product_id, name, price, stock, weight):
        if weight < 0:
            raise ValueError(f"Invalid weight '{weight}'.")
        super().__init__(product_id, name, price, stock)
        self.__weight = float(weight)

    @property
    def weight(self):
        return self.__weight

    def display_information(self, show_tax=False):
        super().display_information(show_tax)
        print(f"    Weight: {self.__weight:.2f} kg")

    def calculate_shipping_cost(self):
        return PhysicalProduct.BASE_SHIPPING_FEE + self.__weight * PhysicalProduct.COST_PER_KG

    def get_fulfilment_info(self):
        return f"Requires physical shipping ({self.__weight:.2f} kg)."

    TYPE = "physical"

    def to_dict(self):
        data = super().to_dict()
        data.update({"type": PhysicalProduct.TYPE, "weight": self.__weight})
        return data
    
    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["name"], data["price"], data["stock"], data["weight"])