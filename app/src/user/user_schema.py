from pydantic import BaseModel
from datetime import datetime


class UserRead(BaseModel):
    id: int
    username: str
    role: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserWrite(BaseModel):
    username: str
    password: str
    role: int
