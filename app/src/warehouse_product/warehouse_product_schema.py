from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from app.src.product.product_schema import ProductRead


class WarehouseProdBase(BaseModel):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class WarehouseProdWrite(BaseModel):
    product_id: int
    status: int
    arrives_at: Optional[datetime]
    quantity: int

    class Config:
        from_attributes = True


class WarehouseProdRead(BaseModel):

    id: int
    product: Optional[ProductRead]
    status: int
    arrives_at: Optional[datetime]
    quantity: int
    created_at: datetime

    class Config:
        from_attributes = True
