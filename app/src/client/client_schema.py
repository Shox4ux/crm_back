from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.src.product.product_schema import ProductRead
from app.src.user.user_schema import UserRead


class ClientProdRead(BaseModel):
    id: int
    custom_price: float
    product: Optional[ProductRead]
    created_at: datetime


class ClientBase(BaseModel):
    user_id: int
    phone: str
    address: str


class ClientWrite(ClientBase):
    pass


class ClientRead(ClientBase):
    id: int
    user: UserRead
    products: Optional[list[ClientProdRead]]
    created_at: datetime

    class Config:
        from_attributes = True
