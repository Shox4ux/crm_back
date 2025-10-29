from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserRead(BaseModel):
    id: int
    username: str
    role: int
    password: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserWrite(BaseModel):
    username: str
    password: str
    hashed_password: Optional[str]
    role: int


class UserUpdt(BaseModel):
    is_active: Optional[bool]
    password: Optional[str]
    hashed_password: Optional[str]
