from product import Product

class DigitalProduct(Product):
    """A product delivered through a download."""

    def __init__(self, product_id, name, price, stock, supplier, download_size):
        if download_size < 0:
            raise ValueError(f"Invalid download size '{download_size}'.")
        super().__init__(product_id, name, price, stock, supplier)
        self.__download_size = float(download_size)

    @property
    def download_size(self):
        return self.__download_size

    def display_information(self, show_tax=False):
        super().display_information(show_tax)
        print(f"    Download Size: {self.__download_size:.2f} MB")

    def get_fulfilment_info(self):
        return f"Delivered digitally via download ({self.__download_size:.2f} MB)."

    TYPE = "digital"

    def to_dict(self):
        data = super().to_dict()
        data.update({"type": DigitalProduct.TYPE, "download_size": self.__download_size})
        return data
    
    @classmethod
    def from_dict(cls, data, supplier):
        return cls(data["id"], data["name"], data["price"], data["stock"], supplier, data["download_size"])