from sqlalchemy import select, insert, delete
from sqlalchemy.exc import SQLAlchemyError
from src.xtuchan.database import async_session_maker
from src.xtuchan.logger import logger


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            try:
                query = insert(cls.model).values(**data).returning(cls.model)
                result = await session.execute(query)
                await session.commit()
                return result.scalar_one()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e

    @classmethod
    async def delete(cls, model_id: int) -> None:
        async with async_session_maker() as session:
            try:
                existing = await cls.find_by_id(model_id)
                if not existing:
                    raise ValueError(f"{cls.model.__name__} with id {model_id} not found")

                query = delete(cls.model).where(cls.model.id == model_id)
                await session.execute(query)
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(
                    f"Error deleting {cls.model.__name__} with id {model_id}: {str(e)}",
                    exc_info=True
                )
                raise e
            except ValueError as e:
                logger.warning(f"Attempt to delete non-existent {cls.model.__name__}: {str(e)}")
                raise e