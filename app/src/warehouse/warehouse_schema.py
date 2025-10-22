from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.src.warehouse_product.warehouse_product_schema import WarehouseProdRead

# warehouse_id = Column(Integer, ForeignKey(f"{tbnames.WAREHOUSE}.id"))
# product_id = Column(Integer, ForeignKey(f"{tbnames.PRODUCT}.id"))
# warehouse = relationship("Warehouse", uselist=False)
# product = relationship("Product", uselist=False)
# status = Column(Integer, nullable=False)
# arrives_at = Column(DateTime, default=func.now())
# quantity = Column(Integer, nullable=False)


class WarehouseBase(BaseModel):
    name: str
    address: Optional[str]


class WarehouseRead(WarehouseBase):
    id: int
    products: Optional[list[WarehouseProdRead]]
    created_at: datetime

    class Config:
        from_attributes = True


class WarehouseWrite(WarehouseBase):
    pass
