from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin, ModelView

from src.xtuchan.features.auth.router import router as users_router
from src.xtuchan.features.products.router import router as product_router
from src.xtuchan.features.reviews.router import router as review_router
from src.xtuchan.features.cart.router import router as cart_router
from src.xtuchan.pydantic_doc import router as pd_router
from src.xtuchan.features.orders.router import router as orders_router
from src.xtuchan.database import engine
from src.xtuchan.features.auth.admin import authentication_backend
from src.xtuchan.features.products.admin import ProductAdmin

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
app.include_router(pd_router)
app.include_router(orders_router)

origins = [
    'http://localhost:3000',
]

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(ProductAdmin)

