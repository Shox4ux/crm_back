from sqlalchemy import String, Column
from sqlalchemy.orm import relationship
from app.utils import table_names as tbnames
from app.models.common_col import ComCharModel


class Factory(ComCharModel):
    __tablename__ = tbnames.FACTORY

    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    wechat = Column(String, nullable=True)
    products = relationship("Product", uselist=True, back_populates="factory")
