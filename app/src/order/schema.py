from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from app.src.order.model import Order
from app.src.order_cancel.schema import OrderCancelResponse
from app.src.order_product.schema import (
    OrderProCreate,
    OrderProUpdate,
    OrderProdResponse,
)
from app.schemas.common_schemas import OrderBase, ClientForOrder
from app.src.admin.schema import AdminResponse


class OrderCreate(BaseModel):
    client_id: int
    status: int
    paid_amount: float
    total_amount: float
    delivery_on: datetime
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
            total_amount=self.total_amount,
            delivery_on=self.delivery_on,
        )


class OrderUpdate(BaseModel):
    status: Optional[int] = None
    paid_amount: Optional[float] = None
    delivery_on: datetime = None
    total_amount: Optional[float] = None
    new_order_products: Optional[list[OrderProCreate]] = None
    updated_order_products: Optional[list[OrderProUpdate]] = None
    deleted_order_products: Optional[list[int]] = None
    admin_note: Optional[str] = None
    client_note: Optional[str] = None

    class Config:
        orm_mode = True


class OrderResponse(OrderBase):
    id: int
    paid_amount: Optional[float] = None
    total_amount: Optional[float] = None
    delivery_on: datetime
    order_products: Optional[list[OrderProdResponse]]
    client: Optional[ClientForOrder]
    cancel_info: Optional[OrderCancelResponse]
    created_at: datetime

    class Config:
        from_attributes = True
