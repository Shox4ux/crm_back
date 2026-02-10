from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.src.product_expense.schema import ProdExpRead
from fastapi import Form, UploadFile
from .model import Product


class ProductBase(BaseModel):
    name: Optional[str]
    base_price: Optional[float]
    sell_price: Optional[float]
    img_url: Optional[str]
    is_archived: Optional[int]
    total_quantity: Optional[int]
    active_quantity: Optional[int]


class ProductUpdate:
    def __init__(
        self,
        img: Optional[UploadFile] = None,
        name: Optional[str] = Form(None),
        base_price: Optional[float] = Form(None),
        sell_price: Optional[float] = Form(None),
        total_quantity: Optional[int] = Form(None),
        is_archived: Optional[int] = Form(None),
    ):
        self.name = name
        self.base_price = base_price
        self.sell_price = sell_price
        self.total_quantity = total_quantity
        self.img = img
        self.is_archived = is_archived

    def to_update(self, img_path: str | None) -> ProductBase:
        return ProductBase(
            name=self.name,
            base_price=self.base_price,
            sell_price=self.sell_price,
            total_quantity=self.total_quantity,
            active_quantity=self.total_quantity,
            img_url=img_path,
            is_archived=self.is_archived,
        )


class ProductCreate:
    def __init__(
        self,
        img: Optional[UploadFile] = None,
        name: str = Form(...),
        base_price: float = Form(...),
        sell_price: float = Form(...),
        total_quantity: int = Form(...),
    ):
        self.name = name
        self.base_price = base_price
        self.sell_price = sell_price
        self.total_quantity = total_quantity
        self.img = img

    def to_prod(self, img_path: str | None) -> Product:
        return Product(
            name=self.name,
            base_price=self.base_price,
            sell_price=self.sell_price,
            total_quantity=self.total_quantity,
            img_url=img_path,
            active_quantity=self.total_quantity,
        )


class ProductSimpleRead(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ProductRead(ProductBase):
    id: int
    base_expenses: Optional[list[ProdExpRead]]
    created_at: datetime

    class Config:
        from_attributes = True


class ProductReadWP(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
