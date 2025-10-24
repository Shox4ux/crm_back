from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from app.src.product.product_schema import ProductRead


class WarehProdBase(BaseModel):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class WarehProdWrite(BaseModel):
    product_id: int
    status: int
    quantity: int

    class Config:
        from_attributes = True


class WarehProdRead(WarehProdBase):

    product: Optional[ProductRead]
    status: int
    arrives_at: Optional[datetime]
    quantity: int

    class Config:
        from_attributes = True
