from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.users.router import router as users_router
from app.products.router import router as product_router
from app.reviews.router import router as review_router
from app.cart.router import router as cart_router


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

app.mount('/static', StaticFiles(directory='app/static'), 'static')

app.include_router(users_router)
app.include_router(product_router)
app.include_router(review_router)
app.include_router(cart_router)

origins = [
    'http://localhost:3000',
]

