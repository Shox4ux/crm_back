from sqlalchemy import String, Column, Float
from app.utils import table_names as tbnames
from app.models.common_col import ComCharModel


class Product(ComCharModel):
    __tablename__ = tbnames.PRODUCT

    name = Column(String(225), nullable=False)
    buy_price = Column(Float, nullable=False)
    sell_price = Column(Float, nullable=False)
    img_url = Column(String, nullable=True)
