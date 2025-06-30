from typing import Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException
from starlette import status
from starlette.responses import Response

from xtuchan.orders.order_service import OrdersService
from xtuchan.orders.repository import OrdersRepository
from xtuchan.orders.schemas import GetOrderSchema, CreateOrderSchema
from xtuchan.orders.exceptions import OrderNotFoundError
from xtuchan.database import async_session_maker

router = APIRouter(
    prefix='',
    tags=['Заказы']
)

@router.get('/orders')
async def get_orders(
        cancelled: Optional[bool] = None,
        limit: Optional[int] = None):
    async with async_session_maker() as session:
        repo = OrdersRepository(session)
        order_service = OrdersService(repo)
        results = await order_service.list_orders(
            limit=limit, cancelled=cancelled
        )
    return {'orders': [result.dict() for result in results]}


@router.post(
    '/orders',
    status_code=status.HTTP_201_CREATED,
    response_model=GetOrderSchema
)
async def create_order(payload: CreateOrderSchema):
    async with async_session_maker() as session:
        repo = OrdersRepository(session)
        order_service = OrdersService(repo)
        order = payload.dict()['order']
        order = await order_service.place_order(order)
        await session.commit()
        return_payload = order.dict()
    return return_payload


@router.get('/orders/{order_id}', response_model=GetOrderSchema)
async def get_order(order_id: UUID):
    try:
        async with async_session_maker() as session:
            repo = OrdersRepository(session)
            order_service = OrdersService(repo)
            order = await order_service.get_order(order_id)
        return order.dict()
    except OrderNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Order with ID {order_id} not found'
        )

@router.put('/orders/{order_id}', response_model=GetOrderSchema)
async def update_order(order_id: UUID, order_details: CreateOrderSchema):
    try:
        async with async_session_maker() as session:
            repo = OrdersRepository(session)
            order_service = OrdersService(repo)
            order = order_details.dict()['order']
            for item in order:
                item['size'] = item['size'].value
            order = await order_service.update_order(
                order_id=order_id, items=order
            )
            await session.commit()
        return order.dict()
    except OrderNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Order with ID {order_id} not found'
        )

@router.delete(
    '/orders/{order_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response
)
async def delete_order(order_id: UUID):
    try:
        async with async_session_maker() as session:
            repo = OrdersRepository(session)
            orders_service = OrdersService(repo)
            await orders_service.delete_order(order_id=order_id)
            await session.commit()
    except OrderNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Order with ID {order_id} not found'
        )

@router.post('/orders/{order_id}/cancel', response_model=GetOrderSchema)
async def cancel_order(order_id: UUID):
    try:
        async with async_session_maker() as session:
            repo = OrdersRepository(session)
            orders_service = OrdersService(repo)
            order = await orders_service.cancel_order(order_id=order_id)
            await session.commit()
        return order.dict()
    except OrderNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Order with ID {order_id} not found'
        )

@router.post('/orders/{order_id}/pay', response_model=GetOrderSchema)
async def pay_order(order_id: UUID):
    try:
        async with async_session_maker() as session:
            repo = OrdersRepository(session)
            orders_service = OrdersService(repo)
            order = await orders_service.pay_order(order_id=order_id)
            await session.commit()
        return order.dict()
    except OrderNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Order with ID {order_id} not found'
        )