from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.src.product.schema import ProductBase


class FactoryBase(BaseModel):
    name: str
    address: Optional[str]
    wechat: Optional[str]
    phone: Optional[str]


class FactoryRead(FactoryBase):
    id: int
    products: Optional[list[ProductBase]]
    created_at: datetime

    class Config:
        from_attributes = True


class FactoryWrite(FactoryBase):
    pass
