from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from src.xtuchan.features.auth.router import router as users_router
from src.xtuchan.features.products.router import router as product_router
from src.xtuchan.features.reviews.router import router as review_router
from src.xtuchan.features.cart.router import router as cart_router
from src.xtuchan.features.orders.router import router as orders_router

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

