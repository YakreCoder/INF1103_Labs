import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from inventory import Inventory
from product_loader import load_products
from supplier import Supplier

CSV_TEXT = """product_type,product_id,name,price,stock_quantity
physical,P001,Desk Lamp,25.00,10
digital,D001,Photo Editor,49.90,100
service,S001,Installation,30.00,5
physical,P002,Office Chair,abc,3
physical,P003,Monitor Stand,39.50,7
"""


class TestLoadProducts(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("S1", "TechSource", "sales@techsource.com")
        self.inventory = Inventory()

    def run_loader(self, path):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            load_products(path, self.inventory, self.supplier)
        return buffer.getvalue()

    def test_bad_rows_skipped_valid_rows_loaded(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "products.csv")
            with open(path, "w", newline="") as f:
                f.write(CSV_TEXT)
            output = self.run_loader(path)
        ids = [p.product_id for p in self.inventory.products]
        self.assertEqual(ids, ["P001", "D001", "P003"])
        self.assertIn("3 products loaded.", output)
        self.assertIn("Load attempt finished.", output)

    def test_missing_file_handled(self):
        output = self.run_loader("does_not_exist.csv")
        self.assertIn("Products file not found", output)
        self.assertNotIn("loaded.", output)
        self.assertIn("Load attempt finished.", output)
        self.assertEqual(self.inventory.products, [])


if __name__ == "__main__":
    unittest.main()