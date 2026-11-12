from product import Product
from supplier import Supplier

class DigitalProduct(Product):
    """A product delivered through a download."""

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                supplier: Supplier, download_size: float) -> None:
        if download_size < 0:
            raise ValueError(f"Invalid download size '{download_size}'.")
        super().__init__(product_id, name, price, stock, supplier)
        self.__download_size = float(download_size)

    @property
    def download_size(self) -> float:
        return self.__download_size

    def display_information(self, show_tax: bool = False) -> None:
        super().display_information(show_tax)
        print(f"    Download Size: {self.__download_size:.2f} MB")

    def get_fulfilment_info(self) -> str:
        return f"Delivered digitally via download ({self.__download_size:.2f} MB)."

    TYPE = "digital"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({"type": DigitalProduct.TYPE, "download_size": self.__download_size})
        return data
    
    @classmethod
    def from_dict(cls, data: dict, supplier: Supplier) -> "DigitalProduct":
        return cls(data["id"], data["name"], data["price"], data["stock"], supplier, data["download_size"])