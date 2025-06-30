from datetime import datetime

from sqlalchemy import Column, Integer, Text, CheckConstraint, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from xtuchan.database import Base


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    text = Column(Text, nullable=True)
    rating = Column(Integer, CheckConstraint('rating BETWEEN 1 AND 5'), nullable=False, default=5)
    created_at = Column(DateTime, default=datetime.utcnow)

    product_rel = relationship("Product", back_populates="reviews")
    __table_args__ = (UniqueConstraint('product_id', 'user_id', name='unique_product_user'),)