import asyncio
import json

import pytest
from sqlalchemy import insert, text

from xtuchan.auth.models import Users
from xtuchan.config import settings
from xtuchan.database import engine, Base, async_session_maker
from xtuchan.products.models import Category, Product

from fastapi.testclient import TestClient
from httpx import AsyncClient

from xtuchan.main import app as fastapi_app


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"src/xtuchan/tests/mock_{model}.json", "r") as file:
            return json.load(file)

    users = open_mock_json("users")
    categories = open_mock_json("categories")
    products = open_mock_json("products")

    async with async_session_maker() as session:
        add_users = insert(Users).values(users)
        add_categories = insert(Category).values(categories)
        add_products = insert(Product).values(products)

        await session.execute(add_users)
        await session.execute(add_categories)
        await session.execute(add_products)
        await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def client():
    yield TestClient(fastapi_app)


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session
