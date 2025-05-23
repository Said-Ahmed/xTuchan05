from typing import Optional, List
from pydantic import BaseModel, Field, field_validator, computed_field
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

    @computed_field
    @property
    def full_image_url(self) -> Optional[str]:
        if not self.image_url:
            return None

        context = getattr(self, "__pydantic_extra__", {})
        if "request" in context:
            return str(context["request"].base_url) + self.image_url

        return self.image_url



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



