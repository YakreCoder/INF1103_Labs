from abc import ABC, abstractmethod

class CanBeShipped(ABC):
    """Interface: any class that can be shipped must calculate a shipping cost."""

    @abstractmethod
    def calculate_shipping_cost(self):
        """Return the shipping cost for this object."""