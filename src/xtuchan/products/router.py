from typing import Optional, List, Annotated

from fastapi import APIRouter, UploadFile, Form, File, Request, HTTPException, Query, Depends, status, Path
from sqlalchemy.exc import SQLAlchemyError
from xtuchan.exceptions import CategoryCannotBeAdded
from xtuchan.auth.permissions import RoleChecker
from xtuchan.products.service import create
from xtuchan.logger import logger
from xtuchan.auth.models import Users
from xtuchan.auth.router import get_current_user
from xtuchan.add_image import add_image
from xtuchan.products.dao import ProductDao, CategoryDao
from xtuchan.products.schemas import SProductCreate, SCategoryCreate, \
    SProductShortResponse, SCategoryResponse, SProductResponse

router = APIRouter(
    prefix='/products',
    tags=['Продукты']
)


@router.post(
    '/add',
    status_code=201,
    dependencies=[Depends(RoleChecker(['admin']))]
)
async def add_product(
    product_in: SProductCreate = Depends(),
    file: UploadFile = File(...),
    request: Request = None
) -> SProductResponse:
    return await create(request, product_in, file)


@router.get("/categories", response_model=List[SCategoryResponse])
async def get_all_categories(request: Request):
    categories = await CategoryDao.find_all()
    for cat in categories:
        if cat.image_url:
            cat.image_url = str(request.base_url) + cat.image_url
    return categories


@router.get("/{product_id}")
async def get_product_by_id(
        product_id: Annotated[int, Path(ge=1)],
        request: Request
) -> SProductResponse:
    product = await ProductDao.find_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Продукт не найден")

    if product.image_url:
        product.image_url = str(request.base_url) + product.image_url
    return product


@router.get("", response_model=List[SProductShortResponse])
async def get_all_products(
    request: Request,
    category_id: int | None = Query(None, ge=1, description="Фильтр по ID категории"),
    min_price: Optional[float] = Query(None, ge=0, description="Минимальная цена"),
    max_price: Optional[float] = Query(None, ge=0, description="Максимальная цена"),
    name: Optional[str] = Query(None, description="Фильтр по названию продукта"),
):
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

    except Exception as e:
        logger.error(msg='2', extra={}, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/category/{category_id}')
async def get_category(category_id: Annotated[int, Path(ge=1)], request: Request) -> SCategoryResponse:
    try:
        cat = await CategoryDao.find_one_or_none(id=category_id)

        if cat and cat.image_url:
            cat.image_url = str(request.base_url) + cat.image_url
        else:
            raise HTTPException(status_code=404, detail="Not found")

        return cat

    except Exception as e:
        raise HTTPException(status_code=404, detail="Not found")

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

    cat = await CategoryDao.add(**category_data.dict())
    if not cat:
        raise CategoryCannotBeAdded

    if cat.image_url:
        cat.image_url = str(request.base_url) + cat.image_url

    return cat


@router.delete('/{product_id}', status_code=204)
async def delete_product(
        product_id: Annotated[int, Path(ge=1)],
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

        return {"message": "Продукт успешно удален"}

    except SQLAlchemyError as e:
        logger.error(f"Ошибка при удалении продукта: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при удалении продукта"
        )


@router.delete('/category/{category_id}', status_code=204)
async def delete_category(
        category_id: Annotated[int, Path(ge=1)],
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

        return {"message": "Категория успешно удалена"}

    except SQLAlchemyError as e:
        logger.error(f"Ошибка при удалении категории: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при удалении категории"
        )



