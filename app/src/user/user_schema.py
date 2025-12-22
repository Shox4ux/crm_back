from pydantic import BaseModel
from typing import Optional
from fastapi import Form, UploadFile
from datetime import datetime


class UserResponse(BaseModel):
    id: Optional[int]
    username: Optional[str] = None
    role: Optional[int] = None
    img: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None
    address: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class UserUpdate:
    def __init__(
        self,
        username: Optional[str] = Form(None),
        password: Optional[str] = Form(None),
        phone: Optional[str] = Form(None),
        is_active: Optional[bool] = Form(None),
        address: Optional[str] = Form(None),
        img: Optional[UploadFile] = None,
    ):
        self.username = username
        self.password = password
        self.phone = phone
        self.address = address
        self.is_active = is_active
        self.img = img
