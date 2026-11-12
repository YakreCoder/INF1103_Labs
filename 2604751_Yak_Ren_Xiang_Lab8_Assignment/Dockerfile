FROM python:3.11-slim

WORKDIR /app

COPY main.py .
COPY product.py .
COPY inventory.py .
COPY inventory.json .
COPY can_be_shipped.py .
COPY physical_product.py .
COPY digital_product.py .
COPY test_products.py .
COPY product_factory.py .
COPY supplier.py .


CMD ["python", "main.py"]