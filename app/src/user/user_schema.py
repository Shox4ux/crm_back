from pydantic import BaseModel
from typing import Optional
from fastapi import Form, UploadFile
from datetime import datetime
from app.src.user.user_model import User
from app.src.auth.auth_method import get_pass_hashed


# Response model (never exposes password/hash)
class UserResponse(BaseModel):
    id: Optional[int]
    username: Optional[str] = None
    role: Optional[int] = None
    img: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# Create schemas using Form (nullable fields for img)
class CreateAsClient:
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

    def to_user(self, img_path) -> User:
        return User(
            username=self.username,
            password_hash=get_pass_hashed(self.password),
            role=0,
            img=img_path,
            phone=self.phone,
            address=self.address,
        )


class CreateAsAdmin:
    def __init__(
        self,
        username: str = Form(...),
        password: str = Form(...),
        img: Optional[UploadFile] = None,
    ):
        self.username = username
        self.password = password
        self.img = img

    def to_user(self, img_path) -> User:
        return User(
            username=self.username,
            password_hash=get_pass_hashed(self.password),
            role=0,
            img=img_path,
        )


# Update schemas (all fields optional)
class UserUpdate:
    def __init__(
        self,
        username: Optional[str] = Form(None),
        password: Optional[str] = Form(None),
        phone: Optional[str] = Form(None),
        address: Optional[str] = Form(None),
        img: Optional[UploadFile] = None,
    ):
        self.username = username
        self.password = password
        self.phone = phone
        self.address = address
        self.img = img
