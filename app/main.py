from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.users.router import router as users_router
from app.products.router import router as product_router
from app.reviews.router import router as review_router
from app.cart.router import router as cart_router


app = FastAPI()

app.mount('/static', StaticFiles(directory='app/static'), 'static')

app.include_router(users_router)
app.include_router(product_router)
app.include_router(review_router)
app.include_router(cart_router)

origins = [
    'http://localhost:3000',
]

