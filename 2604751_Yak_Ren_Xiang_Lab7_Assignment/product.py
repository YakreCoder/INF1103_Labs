from abc import ABC, abstractmethod

class Product(ABC):
    """Represents and manages ONE product (SRP)."""

    TAX_RATE = 0.10

    def __init__(self, product_id, name, price, stock):
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
        self.update_stock(stock)          # reuse validation

    # ---------- read-only access ----------
    @property
    def product_id(self):
        return self.__product_id

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @property
    def stock(self):
        return self.__stock

    # ---------- behaviour ----------
    @staticmethod
    def is_valid_name(name):
        return bool(name) and not name.isdigit()

    def update_stock(self, quantity):
        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity < 0:
            raise ValueError(f"Invalid stock quantity '{quantity}'.")
        self.__stock = quantity

    def calculate_tax(self):
        return self.__price * Product.TAX_RATE * self.__stock

    @abstractmethod
    def get_fulfilment_info(self):
        """Return a string describing how this product is fulfilled."""
        pass

    def display_information(self, show_tax=False):
        line = (f"ID: {self.__product_id} | Name: {self.__name} | "
                f"Price: ${self.__price:.2f} | Stock: {self.__stock}")
        if show_tax:
            line += f" | Tax: ${self.calculate_tax():.2f}"
        print(line)

    # ---------- conversion for JSON (no file I/O here) ----------
    def to_dict(self):
        return {"id": self.__product_id, "name": self.__name,
                "price": self.__price, "stock": self.__stock}
