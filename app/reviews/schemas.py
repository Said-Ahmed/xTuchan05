from typing import Optional

from pydantic import BaseModel, Field

class ReviewCreateSchema(BaseModel):
    rating: int = Field(..., ge=1, le=5, description="Оценка от 1 до 5")
    text: Optional[str] = Field(None, max_length=500, description="Текст отзыва")

class ReviewListSchema(ReviewCreateSchema):
    id: int
    product_id: int
    user_id: int