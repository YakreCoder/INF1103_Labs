from product import Product

class DigitalProduct(Product):
    """A product delivered through a download."""

    def __init__(self, product_id, name, price, stock, download_size):
        if download_size < 0:
            raise ValueError(f"Invalid download size '{download_size}'.")
        super().__init__(product_id, name, price, stock)
        self.__download_size = float(download_size)

    @property
    def download_size(self):
        return self.__download_size

    def display_information(self, show_tax=False):
        super().display_information(show_tax)
        print(f"    Download Size: {self.__download_size:.2f} MB")