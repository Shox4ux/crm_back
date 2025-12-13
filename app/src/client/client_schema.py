from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.src.product.product_schema import ProductRead
from app.src.user.user_schema import UserResponse
from app.schemas.common_schemas import OrderForClient


class ClientProdRead(BaseModel):
    id: int
    custom_price: float
    product: Optional[ProductRead]
    created_at: datetime


class ClientProdWrite(BaseModel):
    client_id: int
    product_id: int
    custom_price: float


class ClientProdUpdt(BaseModel):
    custom_price: float


class ClientResponse(BaseModel):
    id: int
    user: UserResponse
    products: Optional[list[ClientProdRead]]
    orders: Optional[list[OrderForClient]]
    created_at: datetime

    class Config:
        from_attributes = True
