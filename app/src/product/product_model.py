from sqlalchemy import String, Column, Float
from app.utils import table_names as tbnames
from app.models.common_col import ComCharModel
from sqlalchemy.orm import relationship


class Product(ComCharModel):
    __tablename__ = tbnames.PRODUCT

    name = Column(String(225), nullable=False)
    buy_price = Column(Float, nullable=False)
    sell_price = Column(Float, nullable=False)
    img_url = Column(String, nullable=True)
    client_product = relationship(
        "ClientProduct",
        back_populates="product",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
