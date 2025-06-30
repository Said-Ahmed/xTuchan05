from sqlalchemy import Column, Integer, String, Boolean
from xtuchan.database import Base


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

    def __str__(self):
        return f'Пользователь {self.email}'