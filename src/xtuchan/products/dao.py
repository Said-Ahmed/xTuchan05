from sqlalchemy import select, and_

from xtuchan.dao.base import BaseDAO
from xtuchan.database import async_session_maker
from xtuchan.products.models import Product, Category


class ProductDao(BaseDAO):
    model = Product

    @classmethod
    async def find_all(cls, **filters):
        async with async_session_maker() as session:
            query = select(cls.model)

            filter_conditions = []
            for key, value in filters.items():
                if key == "min_price":
                    filter_conditions.append(cls.model.price >= value)
                elif key == "max_price":
                    filter_conditions.append(cls.model.price <= value)
                elif key == "name":
                    filter_conditions.append(cls.model.name.ilike(f"%{value}%"))
                else:
                    filter_conditions.append(getattr(cls.model, key) == value)

            if filter_conditions:
                query = query.where(and_(*filter_conditions))

            result = await session.execute(query)
            return result.scalars().all()


class CategoryDao(BaseDAO):
    model = Category