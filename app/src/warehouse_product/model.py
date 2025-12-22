from sqlalchemy import ForeignKey, DateTime, Column, Integer, func
from sqlalchemy.orm import relationship
from app.utils import table_names as tbnames
from app.models.common_col import ComCharModel


class WarehouseProduct(ComCharModel):
    __tablename__ = tbnames.WAREHOUSE_PRO

    warehouse_id = Column(
        Integer, ForeignKey(f"{tbnames.WAREHOUSE}.id", ondelete="CASCADE")
    )
    product_id = Column(
        Integer, ForeignKey(f"{tbnames.PRODUCT}.id", ondelete="CASCADE")
    )
    product = relationship("Product", uselist=False, lazy="selectin")
    status = Column(Integer, nullable=False)
    arrives_at = Column(DateTime, default=func.now())
    quantity = Column(Integer, nullable=False)
