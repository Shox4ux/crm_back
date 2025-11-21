from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProdExpBase(BaseModel):
    name: str
    amount: float

    class Config:
        from_attributes = True


class ProdExpUpdate(BaseModel):
    id: int
    name: str
    amount: float

    class Config:
        from_attributes = True


class ProdExpWrite(ProdExpBase):
    class Config:
        from_attributes = True

    pass


class ProdExpBulkWrite(BaseModel):
    product_id: int
    items: Optional[list[ProdExpWrite]]

    class Config:
        from_attributes = True

    pass


class ProdExpRead(ProdExpBase):
    id: int
    product_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ProdExpUpdateBulk(BaseModel):
    new_exp: Optional[ProdExpBulkWrite]
    update_exps: Optional[list[ProdExpUpdate]]
    removed: Optional[list[int]]

    class Config:
        from_attributes = True
