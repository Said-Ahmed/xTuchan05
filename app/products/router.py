from typing import Optional

from fastapi import APIRouter, UploadFile, Form, File, Request, HTTPException, Query, Depends, status, Response
from sqlalchemy.exc import SQLAlchemyError

from app.exceptions import ProductCannotBeAdded, CategoryCannotBeAdded
from app.logger import logger
from app.users.models import Users
from app.users.router import get_current_user
from app.utils.add_image import add_image
from app.products.dao import ProductDao, CategoryDao
from app.products.schemas import SProductCreate, SCategoryCreate, SCategoryResponse, \
    SProductShortResponse, SProductDetailResponse

router = APIRouter(
    prefix='/products',
    tags=['Продукты']
)

@router.post('/add')
async def add_product(
    name: str = Form(..., min_length=1, max_length=100),
    description: Optional[str] = Form(None, max_length=500),
    category_id: int = Form(..., gt=0),
    weight: Optional[int] = Form(None, ge=0),
    price: float = Form(..., gt=0),
    file: UploadFile = File(None),
    request: Request = None,
    current_user: Users = Depends(get_current_user)
) -> SProductCreate:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только администраторы могут добавлять продукты"
        )
    try:
        file_name = await add_image(file, request, 'products')

        product_data = SProductCreate(
            name=name,
            category_id=category_id,
            description=description,
            weight=weight,
            price=price,
            image_url=file_name['relative_path'],
        )

        product = await ProductDao.add(**product_data.dict())
        if not product:
            raise ProductCannotBeAdded

        if product.image_url:
            product.image_url = file_name['absolute_url']

        return product

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{product_id}")
async def get_product_by_id(product_id: int) -> SProductDetailResponse:
    try:
        product = await ProductDao.find_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Продукт не найден")
        return product
    except SQLAlchemyError as e:
        raise HTTPException(status_code=404, detail="Произашла непредвиденная ошибка")

@router.get("")
async def get_all_products(
    request: Request,
    category_id: Optional[int] = Query(None, description="Фильтр по ID категории"),
    min_price: Optional[float] = Query(None, description="Минимальная цена"),
    max_price: Optional[float] = Query(None, description="Максимальная цена"),
    name: Optional[str] = Query(None, description="Фильтр по названию продукта"),
) -> list[SProductShortResponse]:
    try:
        filters = {}
        if category_id:
            filters["category_id"] = category_id
        if min_price is not None:
            filters["min_price"] = min_price
        if max_price is not None:
            filters["max_price"] = max_price
        if name:
            filters["name"] = name

        products = await ProductDao.find_all(**filters)
        for product in products:
            if product.image_url:
                product.image_url = str(request.base_url) + product.image_url

        return products

    except (SQLAlchemyError, Exception) as e:
        logger.error(msg='2', extra={}, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/categories')
async def get_all_categories() -> SCategoryResponse:
    try:
        categories = await CategoryDao.find_all()
        if not categories:
            return []
        return categories
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при получении категорий: {str(e)}"
        )


@router.get('/category/category_id/')
async def get_category(category_id: int) -> Optional[SCategoryResponse]:
    return await CategoryDao.find_one_or_none(id=category_id)

@router.post('/category/add')
async def add_category(
        name: str = Form(..., min_length=1, max_length=100),
        file: UploadFile = File(None),
        request: Request = None,
        current_user: Users = Depends(get_current_user)
) -> SCategoryResponse:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только администраторы могут добавлять категории"
        )

    file_name = await add_image(file, request, 'categories')

    category_data = SCategoryCreate(
        name=name,
        image_url=file_name['relative_path'],
    )

    category = await CategoryDao.add(**category_data.dict())
    if not category:
        raise CategoryCannotBeAdded

    if category.image_url:
        category.image_url = file_name['absolute_url']

    return category


@router.delete('/{product_id}')
async def delete_product(
        product_id: int,
        current_user: Users = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только администраторы могут удалять продукты"
        )

    try:
        product = await ProductDao.find_one_or_none(id=product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Продукт не найден"
            )

        await ProductDao.delete(product_id)

        return Response(
            status_code=status.HTTP_200_OK,
            content={"message": "Продукт успешно удален"}
        )
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при удалении продукта: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при удалении продукта"
        )


@router.delete('/category/{category_id}')
async def delete_category(
        category_id: int,
        current_user: Users = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только администраторы могут удалять категории"
        )

    try:
        category = await CategoryDao.find_one_or_none(id=category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Категория не найдена"
            )

        await CategoryDao.delete(category_id)

        return Response(
            status_code=status.HTTP_200_OK,
            content={"message": "Категория успешно удалена"}
        )
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при удалении категории: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при удалении категории"
        )



