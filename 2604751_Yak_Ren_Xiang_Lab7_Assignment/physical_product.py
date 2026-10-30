from product import Product

class PhysicalProduct(Product):
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