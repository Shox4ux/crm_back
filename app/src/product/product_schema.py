from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProdBase(BaseModel):

    name: str
    buy_price: float
    sell_price: float
    img_url: Optional[str]


class ProductWrite(ProdBase):
    pass


class ProductRead(ProdBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
