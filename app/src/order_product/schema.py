from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from app.src.warehouse_product.schema import WareProdRead


class OrderProBase(BaseModel):
    custom_quantity: int
    custom_price: float

    class Config:
        from_attributes = True


class OrderProCreate(OrderProBase):
    warehouse_product_id: int
    product_id: int


class OrderProUpdate(OrderProCreate):
    id: int


class OrderBulkWrite(BaseModel):
    order_id: int
    items: Optional[list[OrderProCreate]]


class OrderProdResponse(OrderProBase):
    id: int
    warehouse_product: Optional[WareProdRead]
    created_at: datetime

    class Config:
        from_attributes = True
