from src.xtuchan.features.orders.exceptions import OrderNotFoundError

class OrdersService:
    def __init__(self, orders_repository):
        self.orders_repository = orders_repository

    async def place_order(self, items):
        return await self.orders_repository.add(items)

    async def get_order(self, order_id):
        order = await self.orders_repository.get(order_id)
        if order is not None:
            return order
        raise OrderNotFoundError(f'Order with id {order_id} not found')

    async def list_orders(self, **filters):
        limit = filters.pop('limit', None)
        return await self.orders_repository.list(limit, **filters)

    async def update_order(self, order_id, items):
        order = await self.orders_repository.get(order_id)
        if order is None:
            raise OrderNotFoundError(f'Order with id {order_id} not found')
        return await self.orders_repository.update(order_id, {'items': items})

    async def delete_order(self, order_id):
        order = await self.orders_repository.get(order_id)
        if order is None:
            raise OrderNotFoundError(f'Order with id {order_id} not found')
        await self.orders_repository.delete(order_id)

    async def pay_order(self, order_id):
        order = await self.orders_repository.get(order_id)
        if order is None:
            raise OrderNotFoundError(f'Order with id {order_id} not found')
        await order.pay()
        schedule_id = await order.schedule()
        return await self.orders_repository.update(
            order_id, {'status': 'schedule', 'schedule_id': schedule_id}
        )

    async def cancel_order(self, order_id):
        order = await self.orders_repository.get(order_id)
        if order is None:
            raise OrderNotFoundError(f'Order with id {order_id} not found')
        await order.cancel()
        return await self.orders_repository.update(order_id, {'status': 'cancelled'})