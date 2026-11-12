from product import Product

class Inventory:
    """Manages a COLLECTION of Product objects (SRP)."""

    STOCK_LIMIT = 500

    def __init__(self) -> None:
        self.__products: list[Product] = []

    @property
    def products(self) -> list[Product]:
        return list(self.__products)      # return a copy to prevent external modification

    def get_unit_count(self) -> int:
        return sum(p.stock for p in self.__products)

    def is_overstocked(self) -> bool:
        return self.get_unit_count() >= Inventory.STOCK_LIMIT

    def find_product(self, product_id: str) -> Product | None:
        for p in self.__products:
            if p.product_id.lower() == product_id.lower():
                return p
        return None

    def add_product(self, product: Product) -> None:
        if self.find_product(product.product_id):
            raise ValueError(f"Product ID '{product.product_id}' already exists.")
        if self.get_unit_count() + product.stock >= Inventory.STOCK_LIMIT:
            raise ValueError(f"Overstock Alert: total stock must stay under "
                             f"{Inventory.STOCK_LIMIT} units.")
        self.__products.append(product)

    def remove_product(self, product_id: str) -> Product:
        # Remove the reference only. The Product itself is NOT destroyed.
        product = self.find_product(product_id)
        if product is None:
            raise ValueError(f"Product ID '{product_id}' not found.")
        self.__products.remove(product)
        return product                    # returned so it can be transferred elsewhere

    def update_stock(self, product_id: str, quantity: int) -> None:
        product = self.find_product(product_id)
        if product is None:
            raise ValueError(f"Product ID '{product_id}' not found.")
        if self.get_unit_count() - product.stock + quantity >= Inventory.STOCK_LIMIT:
            raise ValueError(f"Overstock Alert: total stock must stay under "
                             f"{Inventory.STOCK_LIMIT} units.")
        product.update_stock(quantity)    # Product controls its own state

    def search_product(self, term: str) -> list[Product]:
        term = term.lower()
        if not term:
            return []
        return [p for p in self.__products
                if term in p.product_id.lower() or term in p.name.lower()]

    def display_products(self, products: list[Product], show_tax: bool =False) -> None:
        print("-" * 48)
        for p in products:
            p.display_information(show_tax)
        print("-" * 48, "\n")

    def display_all(self) -> None:
        print("Current Inventory")
        if not self.__products:
            print("-" * 48)
            print("No products in inventory.")
            print("-" * 48, "\n")
        else:
            self.display_products(self.__products)

    def to_list(self) -> list[dict]:
        return [p.to_dict() for p in self.__products]