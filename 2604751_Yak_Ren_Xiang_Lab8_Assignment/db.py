import os
import mysql.connector

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
}
DB_NAME = os.getenv("DB_NAME", "mydb")

SCHEMA = [
    """CREATE TABLE IF NOT EXISTS product (
        product_id   VARCHAR(20)   NOT NULL,
        name         VARCHAR(100)  NOT NULL,
        price        DECIMAL(10,2) NOT NULL,
        stock        INT           NOT NULL,
        product_type VARCHAR(10)   NOT NULL,
        PRIMARY KEY (product_id)
    ) ENGINE=InnoDB""",
    """CREATE TABLE IF NOT EXISTS physical_product (
        product_id VARCHAR(20) NOT NULL,
        weight     DOUBLE      NOT NULL,
        PRIMARY KEY (product_id),
        FOREIGN KEY (product_id) REFERENCES product (product_id)
            ON DELETE CASCADE
    ) ENGINE=InnoDB""",
    """CREATE TABLE IF NOT EXISTS digital_product (
        product_id    VARCHAR(20) NOT NULL,
        download_size DOUBLE      NOT NULL,
        PRIMARY KEY (product_id),
        FOREIGN KEY (product_id) REFERENCES product (product_id)
            ON DELETE CASCADE
    ) ENGINE=InnoDB""",
    """CREATE TABLE IF NOT EXISTS error_log (
        error_id  INT          NOT NULL AUTO_INCREMENT,
        message   VARCHAR(255) NOT NULL,
        logged_at TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (error_id)
    ) ENGINE=InnoDB""",
]


def get_connection():
    """Connect to the server, make sure the schema exists, and select it."""
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`")
    cur.close()
    conn.database = DB_NAME
    return conn


def create_schema(conn):
    cur = conn.cursor()
    for statement in SCHEMA:
        cur.execute(statement)
    conn.commit()
    cur.close()