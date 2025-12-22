from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.src.product.product_schema import ProductRead
from app.src.user.user_schema import UserResponse
from app.schemas.common_schemas import OrderForClient
from fastapi import Form, UploadFile
from app.src.user.user_model import User
from .client_model import Client
from app.src.auth.auth_method import get_pass_hashed


class ClientProdRead(BaseModel):
    id: int
    custom_price: float
    product: Optional[ProductRead]
    created_at: datetime


class ClientProdWrite(BaseModel):
    client_id: int
    product_id: int
    custom_price: float


class ClientProdUpdt(BaseModel):
    custom_price: float


class ClientCreate:
    def __init__(
        self,
        username: str = Form(...),
        password: str = Form(...),
        phone: Optional[str] = Form(None),
        address: Optional[str] = Form(None),
        img: Optional[UploadFile] = None,
    ):
        self.username = username
        self.password = password
        self.phone = phone
        self.address = address
        self.img = img

    def to_user(self, img_path: str | None) -> User:
        return User(
            username=self.username,
            password_hash=get_pass_hashed(self.password),
            role=0,
            img=img_path,
            phone=self.phone,
            address=self.address,
        )

    def to_client(self, user_id: int) -> Client:
        return Client(user_id=user_id)


class ClientResponse(BaseModel):
    id: int
    user: UserResponse
    products: Optional[list[ClientProdRead]]
    orders: Optional[list[OrderForClient]]
    created_at: datetime

    class Config:
        from_attributes = True
