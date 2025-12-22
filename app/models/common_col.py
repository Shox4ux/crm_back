from sqlalchemy import DateTime, Column, Integer, func
from app.data.base import Base


class ComCharModel(Base):
    __abstract__ = True

    id = Column(Integer, autoincrement=True, primary_key=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
