from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.exc import SQLAlchemyError

from src.xtuchan.exceptions import ReviewCannotBeAdded
from src.xtuchan.features.products.dao import ProductDao
from src.xtuchan.logger import logger
from src.xtuchan.features.reviews.dao import ReviewDao
from src.xtuchan.features.reviews.schemas import ReviewCreateSchema, ReviewDetailSchema
from src.xtuchan.features.auth.models import Users
from src.xtuchan.features.auth.router import get_current_user

router = APIRouter(
    prefix='/reviews',
    tags=['Отзывы']
)

@router.post('/{product_id}/add', status_code=201)
async def add_review(
        product_id: Annotated[int, Path(..., ge=1)],
        review_data: ReviewCreateSchema,
        user: Users = Depends(get_current_user)
   ) -> ReviewCreateSchema:
    product = await ProductDao.find_one_or_none(id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Продукт с id {product_id} не найден"
        )
    existing_review = await ReviewDao.find_one_or_none(
        product_id=product_id,
        user_id=user.id
    )
    if existing_review:
        raise HTTPException(
            status_code=400,
            detail="Вы уже оставляли отзыв на этот товар"
        )
    try:
        review = await ReviewDao.add(
            user_id=user.id,
            product_id=product_id,
            text=review_data.text,
            rating=review_data.rating
        )
        if not review:
            raise ReviewCannotBeAdded
        return review
    except Exception as e:
        logger.error(f"Ошибка при создании отзыва: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла ошибка при создании отзыва"
        )


@router.delete('/{review_id}', status_code=204)
async def delete_review(
        review_id: Annotated[int, Path(..., ge=1)],
        current_user: Users = Depends(get_current_user)
):
    review = await ReviewDao.find_one_or_none(id=review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Отзыв не найден"
        )
    if not current_user.is_admin and current_user.id != review.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для выполнения операции"
        )
    try:
        await ReviewDao.delete(model_id=review_id)
    except (SQLAlchemyError, Exception) as e:
        logger.error(f"Ошибка при удалении отзыва: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при удалении отзыва"
        )

@router.get('')
async def get_all_reviews():
    try:
        reviews = await ReviewDao.find_all()
        return {
            "reviews": [ReviewDetailSchema.model_validate(r) for r in reviews]
        }
    except (SQLAlchemyError, Exception) as e:
        logger.error(f"Ощибка при получении отзывов {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при получении отзывов"
        )


@router.get('/{review_id}')
async def get_review_by_id(review_id: int) -> ReviewDetailSchema | None:
    try:
        review = await ReviewDao.find_by_id(review_id)
        return review
    except (SQLAlchemyError, Exception) as e:
        logger.error(f"Ощибка при получении отзывов {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при получении отзывов"
        )