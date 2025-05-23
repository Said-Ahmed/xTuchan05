from enum import StrEnum
from sqlalchemy import Column, Integer, String, Boolean, Enum
from src.xtuchan.database import Base


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    role = Column(
        String,
        nullable=False,
        default='user',
        server_default='user'
    )