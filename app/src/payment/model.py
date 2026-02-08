from sqlalchemy import String, Column, Float, Integer, ForeignKey, DateTime, func
from app.utils import table_names as tbnames
from app.models.common_col import ComCharModel
from sqlalchemy.orm import relationship


class Payment(ComCharModel):
    __tablename__ = tbnames.PAYMENT

    amount = Column(Float, nullable=False)
    method = Column(String(50), nullable=False)
    client_id = Column(Integer, ForeignKey(f"{tbnames.CLIENT}.id", ondelete="CASCADE"))
    client = relationship("Client", uselist=False, lazy="selectin")
    order_id = Column(Integer, ForeignKey(f"{tbnames.ORDER}.id", ondelete="CASCADE"))
    order = relationship("Order", uselist=False, lazy="selectin")
