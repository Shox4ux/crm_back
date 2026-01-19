from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from app.src.order.model import Order
from app.src.order_product.schema import OrderProCreate, OrderProUpdate, OrderProdRead
from app.schemas.common_schemas import OrderBase, ClientForOrder


class OrderCreate(BaseModel):
    client_id: int
    status: int
    paid_amount: float
    order_products: Optional[list[OrderProCreate]]
    admin_note: Optional[str]
    client_note: Optional[str]

    def to_order(self):
        return Order(
            client_id=self.client_id,
            status=self.status,
            paid_amount=self.paid_amount,
            admin_note=self.admin_note,
            client_note=self.client_note,
        )


class OrderUpdate(BaseModel):
    status: Optional[int] = None
    paid_amount: Optional[float] = None
    new_order_products: Optional[list[OrderProCreate]]
    updated_order_products: Optional[list[OrderProUpdate]]
    deleted_order_products: Optional[list[int]]
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
