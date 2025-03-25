from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel, Field


class SProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    category_id: int = Field(..., gt=0)
    weight: Optional[int] = Field(None, ge=0)
    price: float = Field(..., gt=0)
    image_url: str | None

    class Config:
        orm_mode = True


class SProductResponse(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    weight: Optional[int] = Field(None, ge=0)
    price: float = Field(..., gt=0)
    image_url: str | None


class SProductDetailResponse(SProductResponse):
    id: int
    description: str | None


class SProductShortResponse(BaseModel):
    name: str
    price: float
    weight: Optional[int] = None
    image_url: Optional[str] = None

    class Config:
        from_attributes = True


class SCategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=55)
    image_url: str | None


class SCategoryResponse(BaseModel):
    id: int
    name: str
    image_url: str | None

