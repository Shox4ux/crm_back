from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.src.order.schema import OrderResponse
from app.src.client.schema import ClientResponse
from .model import Payment


class PaymentBase(BaseModel):
    amount: Optional[float]
    method: Optional[str]
    client_id: Optional[int]
    order_id: Optional[int]


class PaymentCreate(PaymentBase):

    def to_payment(self):
        return Payment(
            amount=self.amount,
            method=self.method,
            client_id=self.client_id,
            order_id=self.order_id,
        )


class PaymentUpdate(PaymentBase):
    pass


class PaymentResponse(PaymentBase):
    id: int
    # order: Optional[OrderResponse]
    # client: Optional[ClientResponse]
    created_at: datetime

    class Config:
        from_attributes = True
