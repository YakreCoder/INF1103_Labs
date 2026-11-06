import mysql.connector
from db import get_connection, create_schema


class ProductRepository:
    """All SQL lives here (SRP): Inventory and Product never touch the DB."""

    def __init__(self):
        self.__conn = get_connection()
        create_schema(self.__conn)

    def close(self):
        self.__conn.close()

    # ---------- read ----------
    def load_products(self):
        """Return product dicts in the same shape as Product.to_dict()."""
        cur = self.__conn.cursor(dictionary=True)
        cur.execute("""
            SELECT p.product_id AS id, p.name, p.price, p.stock,
                   p.product_type AS type, ph.weight, d.download_size
            FROM product p
            LEFT JOIN physical_product ph ON ph.product_id = p.product_id
            LEFT JOIN digital_product  d  ON d.product_id  = p.product_id
            ORDER BY p.product_id
        """)
        rows = cur.fetchall()
        cur.close()
        return rows

    def load_errors(self):
        cur = self.__conn.cursor()
        cur.execute("SELECT message FROM error_log ORDER BY error_id")
        messages = [row[0] for row in cur.fetchall()]
        cur.close()
        return messages

    # ---------- write ----------
    def save_products(self, product_dicts):
        cur = self.__conn.cursor()
        try:
            for d in product_dicts:
                cur.execute(
                    "INSERT INTO product (product_id, name, price, stock, product_type) "
                    "VALUES (%s, %s, %s, %s, %s) "
                    "ON DUPLICATE KEY UPDATE name = VALUES(name), "
                    "price = VALUES(price), stock = VALUES(stock)",
                    (d["id"], d["name"], d["price"], d["stock"], d["type"]))
                if d["type"] == "physical":
                    cur.execute(
                        "INSERT INTO physical_product (product_id, weight) "
                        "VALUES (%s, %s) ON DUPLICATE KEY UPDATE weight = VALUES(weight)",
                        (d["id"], d["weight"]))
                else:
                    cur.execute(
                        "INSERT INTO digital_product (product_id, download_size) "
                        "VALUES (%s, %s) ON DUPLICATE KEY UPDATE download_size = VALUES(download_size)",
                        (d["id"], d["download_size"]))
            self.__conn.commit()
        except mysql.connector.Error:
            self.__conn.rollback()
            raise
        finally:
            cur.close()

    def save_errors(self, messages):
        cur = self.__conn.cursor()
        try:
            cur.execute("DELETE FROM error_log")
            cur.executemany("INSERT INTO error_log (message) VALUES (%s)",
                            [(m,) for m in messages])
            self.__conn.commit()
        except mysql.connector.Error:
            self.__conn.rollback()
            raise
        finally:
            cur.close()