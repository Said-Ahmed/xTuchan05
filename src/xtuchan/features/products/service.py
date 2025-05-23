from fastapi import Request, HTTPException
from starlette import status

from src.xtuchan.exceptions import ProductCannotBeAdded
from src.xtuchan.features.products.dao import CategoryDao, ProductDao
from src.xtuchan.features.products.schemas import SProductCreate
from src.xtuchan.utils.add_image import add_image


async def create(request: Request, product_in: SProductCreate, file):
    category = await CategoryDao.find_one_or_none(id=product_in.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с ID {product_in.category_id} не найдена"
        )

    file_name = await add_image(file, request, 'products')

    product_data = SProductCreate(
        **product_in.dict(),
        image_url=file_name['relative_path'],
    )

    product = await ProductDao.add(**product_data.dict())
    if not product:
        raise ProductCannotBeAdded

    return product