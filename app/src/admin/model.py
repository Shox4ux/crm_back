from sqlalchemy import Column, Integer, ForeignKey
from app.utils import table_names as tbnames
from app.models.common_col import ComCharModel
from sqlalchemy.orm import relationship


from enum import Enum


class AdminPermission(Enum):
    SUB = 1
    SUPER = 2


class Admin(ComCharModel):
    __tablename__ = tbnames.ADMIN

    user_id = Column(Integer, ForeignKey(f"{tbnames.USER}.id", ondelete="CASCADE"))
    user = relationship("User", uselist=False)
    permission = Column(Integer, nullable=False, default=AdminPermission.SUB.value)
