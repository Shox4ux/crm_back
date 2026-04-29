from pydantic import BaseModel
from datetime import date
from typing import List


class UserInfoDTO(BaseModel):
    full_name: str | None = None
    phone_number: str | None = None


class ClientInfoDTO(BaseModel):
    id: int


class PurchaseDTO(BaseModel):
    date: date
    quantity: int


class ProductDTO(BaseModel):
    id: int
    name: str | None = None
    price: float | None = None


class OrderedProductDTO(BaseModel):
    product: ProductDTO
    purchases: List[PurchaseDTO]


class ClientOrdersDTO(BaseModel):
    client: ClientInfoDTO
    user: UserInfoDTO
    ordered_products: List[OrderedProductDTO]
