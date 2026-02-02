from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.src.warehouse_product.schema import WareProdRead


class WarehouseBase(BaseModel):
    name: str
    address: Optional[str]


class WarehouseRead(WarehouseBase):
    id: int
    products: Optional[list[WareProdRead]]
    created_at: datetime

    class Config:
        from_attributes = True


class WarehouseReadWP(WarehouseBase):
    id: int

    class Config:
        from_attributes = True


class WarehouseWrite(WarehouseBase):
    pass
