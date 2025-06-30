from sqlalchemy import select

from xtuchan.orders.models import OrderModel, OrderItemModel
from xtuchan.orders.orders import Order


class OrdersRepository:
    def __init__(self, session):
        self.session = session

    async def add(self, items):
        record = OrderModel(
            items=[OrderItemModel(**item) for item in items]
        )
        self.session.add(record)
        await self.session.flush()
        return Order(**record.dict(), order_=record)

    async def _get(self, id_, **filters):
        query = select(OrderModel).filter_by(id=str(id_), **filters)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get(self, id_, **filters):
        order = await self._get(id_, **filters)
        if order is not None:
            return Order(**order.dict())

    async def list(self, limit=None, **filters):
        query = select(OrderModel)
        if 'cancelled' in filters:
            cancelled = filters.pop('cancelled')
            if cancelled:
                query = query.where(OrderModel.status == 'cancelled')
            else:
                query = query.where(OrderModel.status != 'cancelled')
        result = await self.session.execute(query)
        records = result.scalars().all()
        return [Order(**record.dict()) for record in records]

    async def update(self, id_, **payload):
        record = await self._get(id_)
        if not record:
            return None

        if 'items' in payload:
            for item in record.items:
                await self.session.delete(item)
            record.items = [
                OrderItemModel(**item) for item in payload.pop('items')
            ]

        for key, value in payload.items():
            setattr(record, key, value)

        await self.session.flush()
        return Order(**record.dict())

    async def delete(self, id_):
        record = await self._get(id_)
        if record:
            await self.session.delete(record)

