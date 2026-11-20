from can_be_shipped import CanBeShipped
from product import Product
from supplier import Supplier

class PhysicalProduct(Product, CanBeShipped):
    """A product that is shipped to the customer."""

    BASE_SHIPPING_FEE = 5.00
    COST_PER_KG = 2.00

    def __init__(self, product_id: str, name: str, price: float, stock: int, 
                 supplier: Supplier, weight: float) -> None:
        if weight < 0:
            raise ValueError(f"Invalid weight '{weight}'.")
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight = float(weight)

    @property
    def weight(self) -> float:
        return self.__weight

    def display_information(self, show_tax: bool = False) -> None:
        super().display_information(show_tax)
        print(f"    Weight: {self.__weight:.2f} kg")

    def calculate_shipping_cost(self) -> float:
        return PhysicalProduct.BASE_SHIPPING_FEE + self.__weight * PhysicalProduct.COST_PER_KG

    def get_fulfilment_info(self) -> str:
        return f"Requires physical shipping ({self.__weight:.2f} kg)."

    TYPE = "physical"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({"type": PhysicalProduct.TYPE, "weight": self.__weight})
        return data
    
    @classmethod
    def from_dict(cls, data: dict, supplier: Supplier) -> "PhysicalProduct":
        return cls(data["id"], data["name"], data["price"], data["stock"], supplier, data["weight"])