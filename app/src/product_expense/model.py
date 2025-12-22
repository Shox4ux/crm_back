from sqlalchemy import String, Column, Float, Integer, ForeignKey
from app.utils import table_names as tbnames
from app.models.common_col import ComCharModel


class ProductExpense(ComCharModel):
    __tablename__ = tbnames.PRODUCT_EXPENS

    product_id = Column(
        Integer, ForeignKey(f"{tbnames.PRODUCT}.id", ondelete="CASCADE")
    )
    name = Column(String(225), nullable=False)
    amount = Column(Float, nullable=False)
