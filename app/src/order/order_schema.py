from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from app.src.order_product.order_product_schema import OrderProdRead
from app.src.client.client_schema import ClientBase


# class Order(ComCharModel):
#     __tablename__ = tbnames.ORDER

#     client_id = Column(Integer, ForeignKey(f"{tbnames.CLIENT}.id"))
#     client = relationship("Client", uselist=False)
#     products = relationship("OrderProduct", uselist=True)
#     status = Column(Integer, nullable=False)
#     client_note = Column(String(425), nullable=True)
#     admin_note = Column(String(425), nullable=True)


class OrderBase(BaseModel):
    status: int
    paid_amount: float
    admin_note: str
    client_note: str

    class Config:
        from_attributes = True


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
    client: Optional[ClientBase]
    created_at: datetime

    class Config:
        from_attributes = True
