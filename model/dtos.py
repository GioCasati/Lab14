from dataclasses import dataclass
from datetime import datetime


@dataclass
class Store:
    store_id: int
    store_name: str
    phone: str
    email: str
    street: str
    city: str
    state: str
    zip_code: int

    def __eq__(self, other):
        return self.store_id == other.store_id

    def __hash__(self):
        return hash(self.store_id)

    def __str__(self):
        return f"{self.store_id} - {self.store_name}"

    def __repr__(self):
        return str(self)

@dataclass
class Ordine:
    order_id: int
    customer_id: int
    order_status: int
    order_date: datetime
    required_date: datetime
    shipped_date: datetime
    store_id: int
    staff_id: int

    def __eq__(self, other):
        return self.order_id == other.order_id

    def __hash__(self):
        return hash(self.order_id)

    def __str__(self):
        return str(self.order_id)

    def __repr__(self):
        return str(self)
