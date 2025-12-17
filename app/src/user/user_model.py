from sqlalchemy import Column, Integer, String, Boolean
from app.models.common_col import ComCharModel
from app.utils import table_names as tbnames


class User(ComCharModel):
    __tablename__ = tbnames.USER

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=True)
    password_hash = Column(String, nullable=True)
    role = Column(Integer, default=0, nullable=True)  # 0 = client, 1 = admin
    img = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=True, default=False)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
