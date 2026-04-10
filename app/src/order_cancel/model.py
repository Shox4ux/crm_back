from sqlalchemy import ForeignKey, String, Column, Integer
from sqlalchemy.orm import relationship
from app.utils import table_names as tbnames
from app.models.common_col import ComCharModel


class OrderCancelInfo(ComCharModel):
    __tablename__ = tbnames.ORDER_CANCEL_INFO

    order_id = Column(Integer, ForeignKey(f"{tbnames.ORDER}.id"))
    order = relationship("Order", uselist=False, back_populates="cancel_info")
    cancel_reason = Column(String, nullable=False)
    cancel_type = Column(Integer, nullable=False)
    canceler_id = Column(Integer, ForeignKey(f"{tbnames.ADMIN}.id"), nullable=False)
    canceler = relationship("Admin", uselist=False)
