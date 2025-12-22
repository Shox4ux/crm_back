from pydantic import BaseModel
from datetime import datetime
from fastapi import Form, UploadFile
from typing import Optional
from app.src.user.user_model import User
from .admin_model import Admin
from app.src.user.user_schema import UserResponse
from app.src.auth.auth_method import get_pass_hashed


class AdminBase(BaseModel):
    user_id: int
    permission: int


class AdminCreate:
    def __init__(
        self,
        username: str = Form(...),
        password: str = Form(...),
        img: Optional[UploadFile] = None,
    ):
        self.username = username
        self.password = password
        self.img = img

    def to_user(self, img_path: str | None) -> User:
        return User(
            username=self.username,
            password_hash=get_pass_hashed(self.password),
            role=1,
            img=img_path,
        )

    def to_admin(self, user_id: int) -> Admin:
        return Admin(user_id=user_id)


class AdminResponse(BaseModel):
    id: int
    permission: int
    user: UserResponse
    created_at: datetime

    class Config:
        from_attributes = True
