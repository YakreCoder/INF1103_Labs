FROM python:3.11-slim

WORKDIR /app

COPY main.py .
COPY product.py .
COPY inventory.py .
COPY inventory.json .
COPY can_be_shipped.py .
COPY physical_product.py .
COPY digital_product.py .
COPY product_factory.py .
COPY supplier.py .
COPY order.py .
COPY discount_strategy.py .
COPY product_loader.py .
COPY products.csv .
COPY lab9_demo.py .
COPY tests/ ./tests/


CMD ["python", "main.py"]