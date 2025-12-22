from sqlalchemy import String, Column, Float, Integer
from app.utils import table_names as tbnames
from app.models.common_col import ComCharModel
from sqlalchemy.orm import relationship


class Product(ComCharModel):
    __tablename__ = tbnames.PRODUCT

    name = Column(String(225), nullable=False)
    base_price = Column(Float, nullable=False)
    sell_price = Column(Float, nullable=False)
    img_url = Column(String, nullable=True)
    measure = Column(Integer, nullable=True)
    total_quantity = Column(Integer, nullable=False)
    active_quantity = Column(Integer, nullable=False)
    base_expenses = relationship(
        "ProductExpense",
        uselist=True,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
