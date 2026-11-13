from product import Product


class OrderLine:
    """One product + quantity inside ONE order.

    Composition: only Order.add_order_line() should create an OrderLine, and a line
    must never be moved to another Order. It refers to a Product but does not own it.
    """

    def __init__(self, product: Product, quantity: int) -> None:
        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
            raise ValueError(f"Invalid order quantity '{quantity}'.")
        self.__product: Product = product
        self.__quantity: int = quantity

    @property
    def product(self) -> Product:
        return self.__product

    @property
    def quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.__product.price * self.__quantity

    def display_information(self) -> None:
        print(f"    {self.__product.name} x {self.__quantity} "
              f"@ ${self.__product.price:.2f} = ${self.calculate_subtotal():.2f}")


class Order:
    """Whole in a composition: creates and manages its own OrderLine objects."""

    def __init__(self, order_id: str) -> None:
        if not str(order_id).strip():
            raise ValueError("Order ID cannot be empty.")
        self.__order_id: str = str(order_id).strip()
        self.__order_lines: list[OrderLine] = []

    @property
    def order_id(self) -> str:
        return self.__order_id

    @property
    def order_lines(self) -> list[OrderLine]:
        return list(self.__order_lines)

    def add_order_line(self, product: Product, quantity: int) -> None:
        # The line is created HERE, never passed in from outside.
        self.__order_lines.append(OrderLine(product, quantity))

    def remove_order_line(self, product_id: str) -> None:
        for line in self.__order_lines:
            if line.product.product_id.lower() == product_id.lower():
                self.__order_lines.remove(line)   # the line is gone; the Product is untouched
                return
        raise ValueError(f"No order line for product '{product_id}'.")

    def calculate_total(self) -> float:
        return sum(line.calculate_subtotal() for line in self.__order_lines)

    def display_information(self) -> None:
        print(f"Order {self.__order_id}")
        for line in self.__order_lines:
            line.display_information()
        print(f"    Total: ${self.calculate_total():.2f}")