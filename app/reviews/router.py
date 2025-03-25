from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError

from app.exceptions import ReviewCannotBeAdded
from app.logger import logger
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


@router.delete('/{review_id}')
async def delete_review(
        review_id: int,
        current_user: Users = Depends(get_current_user)
):
    try:
        review = await ReviewDao.find_one_or_none(id=review_id)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Отзыв не найден"
            )

        if review.user_id != current_user.id and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Вы можете удалять только свои отзывы"
            )

        await ReviewDao.delete(id=review_id)

        return Response(
            status_code=status.HTTP_200_OK,
            content={"message": "Отзыв успешно удален"}
        )
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при удалении отзыва: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при удалении отзыва"
        )

@router.get('')
async def get_all_reviews() -> list[ReviewListSchema]:
    return await ReviewDao.find_all()

@router.get('/{review_id}')
async def get_review_by_id(review_id: int):
    return await ReviewDao.find_by_id(review_id)