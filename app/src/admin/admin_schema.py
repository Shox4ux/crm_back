from pydantic import BaseModel
from datetime import datetime

from app.src.user.user_schema import UserResponse


class AdminBase(BaseModel):
    user_id: int
    permission: int


class AdminWrite(AdminBase):
    pass


class AdminResponse(BaseModel):
    id: int
    permission: int
    user: UserResponse
    created_at: datetime

    class Config:
        from_attributes = True
