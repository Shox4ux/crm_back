from sqlalchemy import ForeignKey, Column, Float, Integer
from app.utils import table_names as tbnames
from app.models.common_col import ComCharModel
from sqlalchemy.orm import relationship


class OrderProduct(ComCharModel):
    __tablename__ = tbnames.ORDER_PRO
    order_id = Column(Integer, ForeignKey(f"{tbnames.ORDER}.id", ondelete="CASCADE"))
    custom_price = Column(Float, nullable=False)
    warehouse_product_id = Column(Integer, ForeignKey(f"{tbnames.WAREHOUSE_PRO}.id"))
    warehouse_product = relationship("WarehouseProduct", uselist=False)
    custom_quantity = Column(Integer, nullable=False)
