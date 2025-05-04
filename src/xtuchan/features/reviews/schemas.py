from typing import Optional, List
from pydantic import Field

from src.xtuchan.schemas import TuchanBase


class ReviewCreateSchema(TuchanBase):
    rating: int = Field(..., ge=1, le=5, description="Оценка от 1 до 5")
    text: Optional[str] = Field(None, max_length=500, description="Текст отзыва")


class ReviewDetailSchema(ReviewCreateSchema):
    id: int
    product_id: int
    user_id: int