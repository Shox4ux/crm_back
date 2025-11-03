from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from app.src.order_product.order_product_schema import OrderProdRead
from app.schemas.common_schemas import OrderBase, ClientForOrder


class OrderWrite(BaseModel):
    client_id: int
    status: int
    paid_amount: float
    admin_note: str
    client_note: str


class OrderUpdt(BaseModel):
    status: Optional[int] = None
    paid_amount: Optional[float] = None
    admin_note: Optional[str] = None
    client_note: Optional[str] = None

    class Config:
        orm_mode = True


class OrderRead(OrderBase):
    id: int
    order_products: Optional[list[OrderProdRead]]
    client: Optional[ClientForOrder]
    created_at: datetime

    class Config:
        from_attributes = True
