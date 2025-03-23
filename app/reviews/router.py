from fastapi import APIRouter, Depends

from app.exceptions import ReviewCannotBeAdded
from app.reviews.dao import ReviewDao
from app.reviews.schemas import ReviewCreateSchema, ReviewListSchema
from app.users.models import Users
from app.users.router import get_current_user

router = APIRouter(
    prefix='/reviews',
    tags=['Отзывы']
)

@router.post('/{product_id}/add')
async def add_review(
        product_id: int,
        review_data: ReviewCreateSchema,
        user: Users = Depends(get_current_user)
   ):
    review = await ReviewDao.add(
        user_id=user.id,
        product_id=product_id,
        text=review_data.text,
        rating=review_data.rating
    )
    if not review:
        raise ReviewCannotBeAdded

@router.get('')
async def get_all_reviews() -> list[ReviewListSchema]:
    return await ReviewDao.find_all()

@router.get('/{review_id}')
async def get_review_by_id(review_id: int):
    return await ReviewDao.find_by_id(review_id)