from sqlalchemy import ForeignKey, String, Column, Integer, Float
from app.utils import table_names as tbnames
from app.models.common_col import ComCharModel
from sqlalchemy.orm import relationship


class Client(ComCharModel):
    __tablename__ = tbnames.CLIENT
    user_id = Column(Integer, ForeignKey(f"{tbnames.USER}.id", ondelete="CASCADE"))
    user = relationship("User", uselist=False)
    phone = Column(String(225), nullable=True)
    address = Column(String(225), nullable=True)
    products = relationship("ClientProduct", uselist=True)
    orders = relationship("Order", uselist=True, back_populates="client")


class ClientProduct(ComCharModel):
    __tablename__ = tbnames.CLIENT_PRO

    product_id = Column(
        Integer, ForeignKey(f"{tbnames.PRODUCT}.id", ondelete="CASCADE")
    )
    client_id = Column(Integer, ForeignKey(f"{tbnames.CLIENT}.id", ondelete="CASCADE"))
    product = relationship("Product", uselist=False, back_populates="client_product")
    custom_price = Column(Float, nullable=False)
