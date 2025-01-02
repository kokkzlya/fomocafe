from __future__ import annotations
from datetime import datetime  # noqa: TCH003

import pydantic

class User(pydantic.BaseModel):
    id: str
    name: str
    email: str
    username: str
    password: str
    created: datetime
    updated: datetime

class Product(pydantic.BaseModel):
    id: str
    name: str
    description: str
    category: str
    price: float
    stock: int
    image_url: str | None
    created: datetime | None
    updated: datetime | None

class Order(pydantic.BaseModel):
    id: int
    table_number: int
    order_items: list[OrderItem]
    created: datetime
    updated: datetime

class OrderItem(pydantic.BaseModel):
    id: int
    product: Product
    quantity: int
    note: str
    created: datetime
    updated: datetime
