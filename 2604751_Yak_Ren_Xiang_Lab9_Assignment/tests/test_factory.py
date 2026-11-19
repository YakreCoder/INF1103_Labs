import unittest
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from product_factory import ProductFactory
from supplier import Supplier


class TestProductFactory(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("S1", "TechSource", "sales@techsource.com")

    def test_creates_physical(self):
        p = ProductFactory.create("physical", "P1", "Lamp", 25.0, 5, self.supplier, 1.5)
        self.assertIsInstance(p, PhysicalProduct)
        self.assertIsInstance(p, Product)

    def test_creates_digital(self):
        p = ProductFactory.create("digital", "D1", "Game", 50.0, 5, self.supplier, 100.0)
        self.assertIsInstance(p, DigitalProduct)

    def test_unknown_type_raises_clear_message(self):
        with self.assertRaises(ValueError) as ctx:
            ProductFactory.create("service", "S1", "Install", 30.0, 5, self.supplier)
        self.assertIn("Unknown product type 'service'", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()