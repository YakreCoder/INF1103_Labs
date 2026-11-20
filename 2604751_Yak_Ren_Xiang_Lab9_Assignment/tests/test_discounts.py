import unittest
from discount_strategy import (DiscountStrategy, NoDiscount, PercentageDiscount,
                               BulkDiscount, StudentDiscount)
from order import Order
from physical_product import PhysicalProduct
from supplier import Supplier


class TestDiscounts(unittest.TestCase):
    def setUp(self):
        supplier = Supplier("S1", "TechSource", "sales@techsource.com")
        product = PhysicalProduct("P1", "Guitar", 250.0, 3, supplier, 4.5)
        self.order = Order("O1")
        self.order.add_order_line(product, 1)          # total = 250

    def test_default_is_no_discount(self):
        self.assertAlmostEqual(self.order.calculate_total(), 250.0)

    def test_bulk_discount(self):
        self.order.set_discount(BulkDiscount(200, 20))
        self.assertAlmostEqual(self.order.calculate_total(), 230.0)

    def test_bulk_below_threshold_unchanged(self):
        self.order.set_discount(BulkDiscount(300, 20))
        self.assertAlmostEqual(self.order.calculate_total(), 250.0)

    def test_set_discount_changes_strategy(self):
        self.order.set_discount(BulkDiscount(200, 20))
        self.order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(self.order.calculate_total(), 225.0)

    def test_student_discount(self):
        self.order.set_discount(StudentDiscount())
        self.assertAlmostEqual(self.order.calculate_total(), 237.5)

    def test_new_strategy_needs_no_order_change(self):
        class HalfPrice(DiscountStrategy):
            def apply(self, total):
                return total / 2
        self.order.set_discount(HalfPrice())
        self.assertAlmostEqual(self.order.calculate_total(), 125.0)

    def test_strategy_is_abstract(self):
        with self.assertRaises(TypeError):
            DiscountStrategy()

    def test_rejects_non_strategy(self):
        with self.assertRaises(TypeError):
            self.order.set_discount("10%")


if __name__ == "__main__":
    unittest.main()