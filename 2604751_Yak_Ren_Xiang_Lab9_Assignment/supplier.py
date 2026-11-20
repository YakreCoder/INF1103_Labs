class Supplier:
    """Who supplies a product. Associated with Product (no ownership)."""

    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:
        if not str(supplier_id).strip():
            raise ValueError("Supplier ID cannot be empty.")
        if not name or name.isdigit():
            raise ValueError(f"Invalid supplier name '{name}'.")
        if "@" not in contact_email:
            raise ValueError(f"Invalid contact email '{contact_email}'.")
        self.__supplier_id: str = str(supplier_id).strip()
        self.__name: str = name
        self.__contact_email: str = contact_email

    @property
    def supplier_id(self) -> str:
        return self.__supplier_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def contact_email(self) -> str:
        return self.__contact_email

    def display_information(self) -> None:
        print(f"Supplier ID: {self.__supplier_id} | Name: {self.__name} | "
              f"Email: {self.__contact_email}")

    def to_dict(self) -> dict:
        return {"supplier_id": self.__supplier_id, "name": self.__name,
                "contact_email": self.__contact_email}

    @classmethod
    def from_dict(cls, data: dict) -> "Supplier":
        return cls(data["supplier_id"], data["name"], data["contact_email"])