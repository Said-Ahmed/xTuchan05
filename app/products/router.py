from typing import Optional

from fastapi import APIRouter, UploadFile, Form, File, Request, HTTPException, Query
from sqlalchemy.exc import SQLAlchemyError

from app.exceptions import ProductCannotBeAdded, CategoryCannotBeAdded
from app.logger import logger
from app.utils.add_image import add_image
from app.products.dao import ProductDao, CategoryDao
from app.products.schemas import SProductCreate, SCategoryCreate, SCategoryResponse, SProductResponse, \
    SProductShortResponse

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
        request: Request = None
) -> SProductResponse:
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
async def get_category() -> SCategoryResponse:
    return await CategoryDao.find_all()

@router.get('/category/category_id/')
async def get_category(category_id: int) -> SCategoryResponse:
    return await CategoryDao.find_one_or_none(id=category_id)

@router.post('/category/add')
async def add_category(
        name: str = Form(..., min_length=1, max_length=100),
        file: UploadFile = File(None),
        request: Request = None
) -> SCategoryResponse:

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


