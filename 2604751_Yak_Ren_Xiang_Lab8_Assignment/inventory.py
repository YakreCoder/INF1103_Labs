class Inventory:
    """Manages a COLLECTION of Product objects (SRP)."""

    STOCK_LIMIT = 500

    def __init__(self):
        self.__products = []

    def get_unit_count(self):
        return sum(p.stock for p in self.__products)

    def is_overstocked(self):
        return self.get_unit_count() >= Inventory.STOCK_LIMIT

    def find_product(self, product_id):
        for p in self.__products:
            if p.product_id.lower() == product_id.lower():
                return p
        return None

    def add_product(self, product):
        if self.find_product(product.product_id):
            raise ValueError(f"Product ID '{product.product_id}' already exists.")
        if self.get_unit_count() + product.stock >= Inventory.STOCK_LIMIT:
            raise ValueError(f"Overstock Alert: total stock must stay under "
                             f"{Inventory.STOCK_LIMIT} units.")
        self.__products.append(product)

    def update_stock(self, product_id, quantity):
        product = self.find_product(product_id)
        if product is None:
            raise ValueError(f"Product ID '{product_id}' not found.")
        if self.get_unit_count() - product.stock + quantity >= Inventory.STOCK_LIMIT:
            raise ValueError(f"Overstock Alert: total stock must stay under "
                             f"{Inventory.STOCK_LIMIT} units.")
        product.update_stock(quantity)    # Product controls its own state

    def search_product(self, term):
        term = term.lower()
        if not term:
            return []
        return [p for p in self.__products
                if term in p.product_id.lower() or term in p.name.lower()]

    def display_products(self, products, show_tax=False):
        print("-" * 48)
        for p in products:
            p.display_information(show_tax)
        print("-" * 48, "\n")

    def display_all(self):
        print("Current Inventory")
        if not self.__products:
            print("-" * 48)
            print("No products in inventory.")
            print("-" * 48, "\n")
        else:
            self.display_products(self.__products)

    def to_list(self):
        return [p.to_dict() for p in self.__products]