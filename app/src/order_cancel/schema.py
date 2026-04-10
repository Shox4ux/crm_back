from pydantic import BaseModel
from datetime import datetime

from app.src.admin.schema import AdminResponse


class OrderCancelCreate(BaseModel):
    order_id: int
    cancel_reason: str
    cancel_type: int
    canceler_id: int


class OrderCancelUpdate(BaseModel):
    cancel_reason: str
    cancel_type: int
    canceler: AdminResponse


class OrderCancelResponse(BaseModel):
    id: int
    cancel_reason: str
    cancel_type: int
    canceler: AdminResponse
    created_at: datetime
