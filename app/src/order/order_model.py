from sqlalchemy import ForeignKey, String, Column, Integer, Float
from sqlalchemy.orm import relationship
from app.utils import table_names as tbnames
from app.models.common_col import ComCharModel


class Order(ComCharModel):
    __tablename__ = tbnames.ORDER

    client_id = Column(Integer, ForeignKey(f"{tbnames.CLIENT}.id"))
    client = relationship("Client", uselist=False)
    order_products = relationship("OrderProduct", uselist=True)
    status = Column(Integer, nullable=False)
    paid_amount = Column(Float, nullable=False)
    client_note = Column(String(425), nullable=True)
    admin_note = Column(String(425), nullable=True)
