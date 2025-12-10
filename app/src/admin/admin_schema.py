from pydantic import BaseModel
from datetime import datetime

# from app.src.user.user_schema import UserRead


class AdminBase(BaseModel):
    user_id: int
    permission: int


class AdminWrite(AdminBase):
    pass


class AdminRead(BaseModel):
    id: int
    permission: int
    # user: UserRead
    created_at: datetime

    class Config:
        from_attributes = True
