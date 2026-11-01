from physical_product import PhysicalProduct
from digital_product import DigitalProduct

PRODUCT_TYPES = {
    PhysicalProduct.TYPE: PhysicalProduct,
    DigitalProduct.TYPE: DigitalProduct,
}


def create_product(data):
    product_class = PRODUCT_TYPES.get(data["type"])
    if product_class is None:
        raise ValueError(f"Unknown product type '{data['type']}'.")
    return product_class.from_dict(data)