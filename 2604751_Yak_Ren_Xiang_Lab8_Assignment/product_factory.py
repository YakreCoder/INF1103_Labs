from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier

PRODUCT_TYPES = {
    PhysicalProduct.TYPE: PhysicalProduct,
    DigitalProduct.TYPE: DigitalProduct,
}


def create_product(data, suppliers):
    product_class = PRODUCT_TYPES.get(data["type"])
    if product_class is None:
        raise ValueError(f"Unknown product type '{data['type']}'.")
    supplier = suppliers.get(data["supplier_id"])
    if supplier is None:
        raise ValueError(f"Unknown supplier '{data['supplier_id']}'.")
    return product_class.from_dict(data, supplier)