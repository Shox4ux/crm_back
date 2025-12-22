from sqlalchemy import String, Column
from sqlalchemy.orm import relationship
from app.utils import table_names as tbnames
from app.models.common_col import ComCharModel


class Warehouse(ComCharModel):
    __tablename__ = tbnames.WAREHOUSE

    name = Column(String(225), nullable=False)
    address = Column(String(225), nullable=True)
    products = relationship(
        "WarehouseProduct",
        uselist=True,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
