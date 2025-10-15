from sqlalchemy import ForeignKey, String, Column, Integer
from sqlalchemy.orm import relationship
from app.utils import table_names as tbnames
from app.models.common_col import ComCharModel


class OrderProduct(ComCharModel):
    __tablename__ = tbnames.ORDER_PRO
    client_product_id = Column(Integer, ForeignKey(f"{tbnames.CLIENT_PRO}.id"))
    client_product = relationship("ClientProduct", uselist=False)
    sold_quantity = Column(Integer, nullable=False)
    warehouse_product_id = Column(Integer, ForeignKey(f"{tbnames.WAREHOUSE_PRO}.id"))
    warehouse_product = relationship("WarehouseProduct", uselist=False)
    order_id = Column(Integer, ForeignKey(f"{tbnames.ORDER}.id"))


class Order(ComCharModel):
    __tablename__ = tbnames.ORDER

    client_id = Column(Integer, ForeignKey(f"{tbnames.CLIENT}.id"))
    ordered_products = relationship("OrderProduct", uselist=True)
    status = Column(Integer, nullable=False)
    client_note = Column(String(425), nullable=True)
    admin_note = Column(String(425), nullable=True)
