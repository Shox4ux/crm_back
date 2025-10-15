from sqlalchemy import Column, Integer, String
from app.models.common_col import ComCharModel
from app.utils import table_names as tbnames


class User(ComCharModel):
    __tablename__ = tbnames.USER

    role = Column(Integer, nullable=False)
    username = Column(String(225), nullable=False)
    password = Column(String(225), nullable=False)
