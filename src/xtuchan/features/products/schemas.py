from typing import Optional, List
from pydantic import BaseModel, Field, Extra, model_validator
from src.xtuchan.schemas import TuchanBase

class SProductCreate(TuchanBase):
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    category_id: int = Field(gt=0)
    weight: Optional[int] = Field(None, ge=0, le=10000)
    price: float = Field(gt=0)


class SProductDetailResponse(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=100)
    weight: Optional[int] = Field(None, ge=0)
    price: float = Field(..., gt=0)
    image_url: str | None
    description: str | None


class SProductShortResponse(TuchanBase):
    id: int
    name: str
    price: float
    weight: Optional[int] = None
    image_url: Optional[str] = None

    class Config:
        orm_mode = True


class SProductListResponse(BaseModel):
    items: List[SProductShortResponse]
    count: int


class SCategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=55)
    image_url: str | None


class CategorySchema(TuchanBase):
    id: int
    name: str
    image_url: Optional[str] = None

    class Config:
        from_attributes = True



