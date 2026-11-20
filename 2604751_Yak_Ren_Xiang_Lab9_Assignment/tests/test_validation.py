import unittest
from physical_product import PhysicalProduct
from order import Order
from supplier import Supplier


class TestValidation(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("S1", "TechSource", "sales@techsource.com")
        self.product = PhysicalProduct("P1", "Lamp", 25.0, 5, self.supplier, 1.0)

    def test_price_zero_rejected(self):
        with self.assertRaises(ValueError):
            PhysicalProduct("P2", "Free", 0, 1, self.supplier, 1.0)

    def test_price_negative_rejected(self):
        with self.assertRaises(ValueError):
            PhysicalProduct("P2", "Bad", -5, 1, self.supplier, 1.0)

    def test_negative_stock_rejected_on_create(self):
        with self.assertRaises(ValueError):
            PhysicalProduct("P2", "Bad", 5.0, -1, self.supplier, 1.0)

    def test_negative_stock_rejected_on_update(self):
        with self.assertRaises(ValueError):
            self.product.update_stock(-1)

    def test_order_quantity_must_be_positive(self):
        order = Order("O1")
        for bad in (0, -3):
            with self.assertRaises(ValueError):
                order.add_order_line(self.product, bad)


if __name__ == "__main__":
    unittest.main()