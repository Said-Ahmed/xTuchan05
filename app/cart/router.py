from cachetools import TTLCache
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select

from app.cart.schemas import CartItemResponse, CartResponse
from app.database import async_session_maker
from app.products.dao import ProductDao
from app.products.models import Product
from app.products.schemas import SProductShortResponse
from app.users.models import Users
from app.users.router import get_current_user

router = APIRouter(
    prefix='/cart',
    tags=['Корзина'],
)

carts_cache = TTLCache(maxsize=1000, ttl=604800)


@router.post("/add")
async def add_to_cart(
    request: Request,
    product_id: int,
    user: Users = Depends(get_current_user),
) -> SProductShortResponse:
    try:
        product = await ProductDao.find_by_id(product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Product not found"})

        cart = carts_cache.get(user.id, {})
        cart[product_id] = cart.get(product_id, 0) + 1
        carts_cache[user.id] = cart

        product.image_url = str(request.base_url) + product.image_url

        return product

    except Exception as e:
        print(e)
        raise HTTPException(status_code=404)


@router.get("")
async def get_cart(
    request: Request,
    user: Users = Depends(get_current_user),
):
    try:
        cart = carts_cache.get(user.id)

        if not cart:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Cart is empty"})

        product_ids = list(cart.keys())
        query = select(Product).where(Product.id.in_(product_ids))
        total_sum = 0.0
        items = []

        async with async_session_maker() as session:
            result = await session.execute(query)
            products = result.scalars().all()

            for product in products:
                quantity = cart[product.id]
                total_sum += float(product.price) * quantity

                if product.image_url:
                    product.image_url = str(request.base_url) + product.image_url

                items.append(CartItemResponse(
                    product_id=product.id,
                    name=product.name,
                    price=product.price,
                    weight=product.weight,
                    image_url=product.image_url,
                    quantity=quantity,
                ))

        return CartResponse(user_id=user.id, items=items, total_sum=total_sum)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@router.delete("/remove/{product_id}")
async def remove_from_cart(
    product_id: int,
    user: Users = Depends(get_current_user),
):
    try:
        cart = carts_cache.get(user.id)

        if not cart:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Cart is empty"})

        if product_id in cart:
            if cart[product_id] > 1:
                cart[product_id] -= 1
            else:
                del cart[product_id]

            carts_cache[user.id] = cart
            return {"message": "Product removed from cart"}
        else:
            raise HTTPException(status_code=404, detail={"message": "Product not found in cart"})

    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Cart is empty"})

@router.delete("/clear")
async def clear_cart(
    user: Users = Depends(get_current_user),
):
    try:
        if user.id in carts_cache:
            del carts_cache[user.id]

        return {"message": "Cart cleared successfully"}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")