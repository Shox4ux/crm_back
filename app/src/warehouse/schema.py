from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.schemas.common_schemas import GlobalWarePro


class WarehouseBase(BaseModel):
    name: str
    address: Optional[str]


class WarehouseRead(WarehouseBase):
    id: int
    products: Optional[list[GlobalWarePro]]
    created_at: datetime

    class Config:
        from_attributes = True


class WarehouseReadWP(WarehouseBase):
    id: int
    created_at: datetime
    pass


class WarehouseWrite(WarehouseBase):
    pass
