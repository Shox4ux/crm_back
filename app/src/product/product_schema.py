from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.src.product_expense.product_expense_schema import ProdExpRead, ProdExpWrite


class ProdBase(BaseModel):
    name: str
    base_price: float
    sell_price: float
    img_url: Optional[str]
    total_quantity: int
    active_quantity: int


class ProductWrite(ProdBase):
    pass


class ProductSimpleRead(ProdBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ProductRead(ProdBase):
    id: int
    base_expenses: Optional[list[ProdExpRead]]
    created_at: datetime

    class Config:
        from_attributes = True
