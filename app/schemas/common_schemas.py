from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.src.user.schema import UserResponse
from app.src.order_product.schema import OrderProdResponse
from app.src.product.schema import ProductReadWP


class ClientPrRead(BaseModel):
    id: int
    custom_price: float
    # product: Optional[ProductRead]
    created_at: datetime


class OrderBase(BaseModel):
    id: int
    status: int
    paid_amount: float
    admin_note: str
    client_note: str
    created_at: datetime

    class Config:
        from_attributes = True


class OrderForClient(OrderBase):
    id: int
    order_products: Optional[list[OrderProdResponse]]

    class Config:
        from_attributes = True


class ClientForOrder(BaseModel):
    id: int
    user: UserResponse
    products: Optional[list[ClientPrRead]]
    created_at: datetime

    class Config:
        from_attributes = True


class GlobalWarePro(BaseModel):
    product: Optional[ProductReadWP]
    warehouse_id: int
    status: int
    arrives_at: Optional[datetime]
    quantity: int

    class Config:
        from_attributes = True
