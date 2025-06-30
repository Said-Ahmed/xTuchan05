from fastapi import Request, HTTPException
from starlette import status

from xtuchan.exceptions import ProductCannotBeAdded
from xtuchan.products.dao import CategoryDao, ProductDao
from xtuchan.products.schemas import SProductCreate
from xtuchan.add_image import add_image


async def create(request: Request, product_in: SProductCreate, file):
    category = await CategoryDao.find_one_or_none(id=product_in.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с ID {product_in.category_id} не найдена"
        )

    file_name = await add_image(file, request, 'products')

    product = await ProductDao.add(**product_in.dict(), image_url=file_name['relative_path'],)
    if not product:
        raise ProductCannotBeAdded

    if product.image_url:
        product.image_url = str(request.base_url) + product.image_url

    return product