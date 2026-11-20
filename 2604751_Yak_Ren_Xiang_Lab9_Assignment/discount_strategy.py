from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """Interface: one interchangeable way of discounting an order total."""

    @abstractmethod
    def apply(self, total: float) -> float:
        """Return the discounted total."""


class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float) -> None:
        if not 0 <= percentage <= 100:
            raise ValueError(f"Invalid percentage '{percentage}'.")
        self.__percentage = percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.__percentage / 100)


class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, amount: float) -> None:
        if threshold < 0 or amount < 0:
            raise ValueError("Threshold and amount cannot be negative.")
        self.__threshold = threshold
        self.__amount = amount

    def apply(self, total: float) -> float:
        return max(0.0, total - self.__amount) if total >= self.__threshold else total


class StudentDiscount(PercentageDiscount):
    """Fourth strategy (2.4): a fixed 5% off. Order needs no changes."""

    def __init__(self) -> None:
        super().__init__(5)