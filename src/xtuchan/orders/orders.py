import httpx
from xtuchan.orders.exceptions import APIIntegrationError


class OrderItem:
    def __init__(self, id, product, quantity, size):
        self.id = id
        self.product = product
        self.quantity = quantity
        self.size = size

    def dict(self):
        return {
            'id': self.id,
            'product': self.product,
            'quantity': self.quantity,
            'size': self.size
        }

class Order:
    def __init__(self, id, created, items, status, schedule_id=None, delivery_id=None, order_=None):
        self._id = id
        self._created = created
        self.items = [OrderItem(**item) for item in items]
        self._status = status
        self.schedule_id = schedule_id
        self.delivery_id = delivery_id
        self.order_ = order_

    @property
    def id(self):
        return self._id or self.order_.id

    @property
    def created(self):
        return self._created or self.order_.created

    @property
    def status(self):
        return self._status or self.order_.status

    async def cancel(self):
        if self.status == 'progress':
            async with httpx.AsyncClient() as client:
                kitchen_base_url = 'localhost:8000/kitchen'
                response = await client.post(
                    f'{kitchen_base_url}/schedules/{self.schedule_id}/cancel',
                    json={"order": [item.dict() for item in self.items]},
                )
                if response.status_code == 200:
                    return
                raise APIIntegrationError(
                    f'Could not cancel order with id {self.id}'
                )
        if self.status == 'delivery':
            raise APIIntegrationError(
                f'Cannot cancel order with id {self.id} during delivery'
            )

    async def pay(self):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                'localhost:8000/payments',
                json={'order_id': str(self.id)}
            )
            if response.status_code == 201:
                return
            raise APIIntegrationError(
                f'Could not process payment for order with id {self.id}'
            )

    async def schedule(self):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                'localhost:8000/schedules/',
                json={"order": [item.dict() for item in self.items]},
            )
            if response.status_code == 201:
                return response.json()['id']
            raise APIIntegrationError(
                f'Could not schedule order with id {self.id}'
            )

    def dict(self):
        return {
            'id': self.id,
            'created': self.created,
            'items': [item.dict() for item in self.items],
            'status': self.status,
            'schedule_id': self.schedule_id,
            'delivery_id': self.delivery_id
        }