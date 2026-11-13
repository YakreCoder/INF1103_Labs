from abc import ABC, abstractmethod
from supplier import Supplier

class Product(ABC):
    """Represents and manages ONE product (SRP)."""

    TAX_RATE = 0.10

    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier) -> None:
        if supplier is None:
            raise ValueError("A product must have a valid supplier.")
        if not str(product_id).strip():
            raise ValueError("Product ID cannot be empty.")
        if not Product.is_valid_name(name):
            raise ValueError(f"Invalid product name '{name}'.")
        if price < 0:
            raise ValueError(f"Invalid price '{price}'.")

        self.__product_id = str(product_id).strip()
        self.__name = name
        self.__price = float(price)
        self.__stock = 0
        self.__supplier: Supplier = supplier
        self.update_stock(stock)          # reuse validation

    # ---------- read-only access ----------
    @property
    def product_id(self) -> str:
        return self.__product_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def price(self) -> float:
        return self.__price

    @property
    def stock(self) -> int:
        return self.__stock

    @property
    def supplier(self) -> Supplier:
        return self.__supplier

    # ---------- behaviour ----------
    @staticmethod
    def is_valid_name(name: str) -> bool:
        return bool(name) and not name.isdigit()

    def update_stock(self, quantity: int) -> None:
        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity < 0:
            raise ValueError(f"Invalid stock quantity '{quantity}'.")
        self.__stock = quantity

    def calculate_tax(self) -> float:
        return self.__price * Product.TAX_RATE * self.__stock

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Return a string describing how this product is fulfilled."""
        pass

    def display_information(self, show_tax: bool = False) -> None:
        line = (f"ID: {self.__product_id} | Name: {self.__name} | "
                f"Price: ${self.__price:.2f} | Stock: {self.__stock}")
        if show_tax:
            line += f" | Tax: ${self.calculate_tax():.2f}"
        print(line)
        print(f"    Supplier: {self.__supplier.name}")

    # ---------- conversion for JSON (no file I/O here) ----------
    def to_dict(self) -> dict:
        return {"id": self.__product_id, "name": self.__name,
                "price": self.__price, "stock": self.__stock,
                "supplier_id": self.__supplier.supplier_id}
