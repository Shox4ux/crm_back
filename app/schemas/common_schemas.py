from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.src.product.product_schema import ProductRead
from app.src.user.user_schema import UserRead
from app.src.order_product.order_product_schema import OrderProdRead


class ClientBase(BaseModel):
    phone: str
    address: str

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    status: int
    paid_amount: float
    admin_note: str
    client_note: str

    class Config:
        from_attributes = True


class OrderForClient(OrderBase):
    id: int
    order_products: Optional[list[OrderProdRead]]
    created_at: datetime

    class Config:
        from_attributes = True
