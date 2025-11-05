from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from app.src.warehouse_product.warehouse_product_schema import WareProdRead


class OrderProdBase(BaseModel):
    custom_quantity: int
    custom_price: float

    class Config:
        from_attributes = True


class OrderProdWrite(OrderProdBase):
    warehouse_product_id: int


class OrderBulkWrite(BaseModel):
    order_id: int
    items: Optional[list[OrderProdWrite]]


class OrderProdRead(OrderProdBase):
    id: int
    warehouse_product: Optional[WareProdRead]
    created_at: datetime

    class Config:
        from_attributes = True
