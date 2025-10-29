from sqlalchemy import ForeignKey, String, Column, Integer
from app.utils import table_names as tbnames
from app.models.common_col import ComCharModel
from sqlalchemy.orm import relationship


class Client(ComCharModel):
    __tablename__ = tbnames.CLIENT
    user_id = Column(Integer, ForeignKey(f"{tbnames.USER}.id", ondelete="CASCADE"))
    user = relationship(
        "User",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    phone = Column(String(225), nullable=True)
    address = Column(String(225), nullable=True)
    products = relationship(
        "ClientProduct",
        uselist=True,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class ClientProduct(ComCharModel):
    __tablename__ = tbnames.CLIENT_PRO

    product_id = Column(Integer, ForeignKey(f"{tbnames.PRODUCT}.id"))
    client_id = Column(Integer, ForeignKey(f"{tbnames.CLIENT}.id", ondelete="CASCADE"))
    product = relationship("Product", uselist=False)
    custom_price = Column(String(225), nullable=False)
