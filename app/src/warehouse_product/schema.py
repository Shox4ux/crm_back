from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from app.src.product.schema import ProductReadWP


class WareProdBase(BaseModel):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class WareProdWrite(BaseModel):
    warehouse_id: int
    product_id: int
    status: int
    quantity: int

    class Config:
        from_attributes = True


class WareProdUpdate(BaseModel):
    id: int
    status: int
    quantity: int


class GlobalWarehouse(BaseModel):
    id: int
    address: str
    name: str
    created_at: datetime

    class Config:
        from_attributes = True


class WareProdRead(WareProdBase):
    product: Optional[ProductReadWP]
    warehouse_id: int
    warehouse: Optional[GlobalWarehouse]
    status: int
    arrives_at: Optional[datetime]
    quantity: int

    class Config:
        from_attributes = True


class InnerWareProdRead(WareProdBase):
    product: Optional[ProductReadWP]
    status: int
    arrives_at: Optional[datetime]
    quantity: int

    class Config:
        from_attributes = True
