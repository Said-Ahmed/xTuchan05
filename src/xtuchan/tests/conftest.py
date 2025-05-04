import pytest

from src.xtuchan.config import settings
from src.xtuchan.database import engine, Base


@pytest.fixture(autouse=True)
async def prepare_database():
    assert settings.MODE == 'TEST'

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
