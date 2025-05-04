from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, CheckConstraint, Text
from sqlalchemy.orm import relationship

from src.xtuchan.database import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    category_id = Column(ForeignKey('categories.id', ondelete='RESTRICT'), nullable=False, index=True)
    description = Column(Text, nullable=True)
    weight = Column(Integer, CheckConstraint('weight >= 0'), nullable=True)
    price = Column(Numeric(precision=10, scale=2), nullable=False)
    image_url = Column(String(255), nullable=True)

    reviews = relationship("Review", back_populates="product_rel")
    category_rel = relationship("Category", back_populates="products")


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(55), nullable=False)
    image_url = Column(String(255), nullable=True)

    products = relationship("Product", back_populates="category_rel")


