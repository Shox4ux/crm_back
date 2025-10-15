from sqlalchemy import ForeignKey, DateTime, String, Column, Integer, func
from sqlalchemy.orm import relationship
from app.utils import table_names as tbnames
from app.models.common_col import ComCharModel


class Warehouse(ComCharModel):
    __tablename__ = tbnames.WAREHOUSE

    name = Column(String(225), nullable=False)
    address = Column(String(225), nullable=True)
    products = relationship("WarehouseProduct", uselist=True)


class WarehouseProduct(ComCharModel):
    __tablename__ = tbnames.WAREHOUSE_PRO

    warehouse_id = Column(Integer, ForeignKey(f"{tbnames.WAREHOUSE}.id"))
    product_id = Column(Integer, ForeignKey(f"{tbnames.PRODUCT}.id"))
    warehouse = relationship("Warehouse", uselist=False)
    product = relationship("Product", uselist=False)
    status = Column(Integer, nullable=False)
    arrives_at = Column(DateTime, default=func.now())
    quantity = Column(Integer, nullable=False)
