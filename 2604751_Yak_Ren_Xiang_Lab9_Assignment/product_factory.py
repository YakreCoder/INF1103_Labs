from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier
from product import Product

PRODUCT_TYPES = {
    PhysicalProduct.TYPE: PhysicalProduct,
    DigitalProduct.TYPE: DigitalProduct,
}

class ProductFactory:
    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock_quantity: int, supplier: Supplier,  specific_value: float = 0.0) -> Product:
        product_class = PRODUCT_TYPES.get(product_type)
        if product_class is None:
            raise ValueError(f"Unknown product type '{product_type}'.")
        return product_class(product_id, name, price, stock_quantity, supplier, specific_value)



def create_product(data: dict, suppliers: dict[str, Supplier]) -> Product:
    product_class = PRODUCT_TYPES.get(data["type"])
    if product_class is None:
        raise ValueError(f"Unknown product type '{data['type']}'.")
    supplier = suppliers.get(data["supplier_id"].lower())
    if supplier is None:
        raise ValueError(f"Unknown supplier '{data['supplier_id']}'.")
    return product_class.from_dict(data, supplier)