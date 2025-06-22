from typing import Optional, List
from pydantic import BaseModel, Field, field_validator, computed_field, model_validator
from src.xtuchan.schemas import TuchanBase


class SProductCreate(TuchanBase):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)
    category_id: int = Field(gt=0)
    weight: int | None  = Field(None, ge=0, le=10000)
    price: float = Field(gt=0)


class SProductResponse(TuchanBase):
    name: str
    description: str | None
    category_id: int
    weight: int | None
    price: float
    image_url: str


class SProductShortResponse(TuchanBase):
    id: int
    name: str
    price: float
    weight: int | None = None
    image_url: str


class SProductListResponse(TuchanBase):
    items: List[SProductShortResponse]

    @computed_field
    @property
    def count(self) -> int:
        return len(self.items)


class SCategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=55)
    image_url: str


class SCategoryResponse(TuchanBase):
    id: int
    name: str
    image_url: str




