from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.src.order.schema import OrderResponse
from app.src.client.schema import ClientBase
from app.schemas.common_schemas import OrderBase
from .model import Payment


class PaymentBase(BaseModel):
    amount: Optional[float]
    method: Optional[str]


class PaymentCreate(PaymentBase):
    client_id: Optional[int]
    order_id: Optional[int]

    def to_payment(self):
        return Payment(
            amount=self.amount,
            method=self.method,
            client_id=self.client_id,
            order_id=self.order_id,
        )


class PaymentUpdate(PaymentBase):
    client_id: Optional[int]
    order_id: Optional[int]
    pass


class PaymentResponse(PaymentBase):
    id: int
    order: Optional[OrderBase]
    client: Optional[ClientBase]
    created_at: datetime

    class Config:
        from_attributes = True
