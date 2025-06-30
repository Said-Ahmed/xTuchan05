from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from xtuchan.auth.router import router as users_router
from xtuchan.products.router import router as product_router
from xtuchan.reviews.router import router as review_router
from xtuchan.cart.router import router as cart_router
from xtuchan.orders.router import router as orders_router

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount('/static', StaticFiles(directory='src/xtuchan/static'), 'static')

app.include_router(users_router)
app.include_router(product_router)
app.include_router(review_router)
app.include_router(cart_router)
app.include_router(orders_router)

