from pydantic import BaseModel
from datetime import datetime


class AdminBase(BaseModel):
    user_id: int
    permission: int


class AdminWrite(AdminBase):
    pass


class AdminRead(AdminBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
