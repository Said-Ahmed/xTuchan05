from enum import Enum
from typing import Annotated

from fastapi import APIRouter, Request, File
from fastapi.params import Path, Query
from pydantic import BaseModel, Field

router = APIRouter(
    prefix='/api',
    tags=['API']
)

@router.get('/items_validated/{request_id}')
async def read_item(request_id: Annotated[int, Path(ge=10, lt=15)]):
    return {"request_id": request_id}


class RequestTypes(str, Enum):
    service = 'service'
    new_feature = 'new_feature'


@router.get('/request/type/{request_type}')
async def read_item(request_type: RequestTypes):
    return {"request_type": request_type.value}


@router.get('/query_params_default')
async def read_item(req: Annotated[str, Query(min_length=5, max_length=25, pattern='test*')] = 'test_default_string'):
    return {
        "req": req
    }

@router.get('/query_params_list_default')
async def read_items(q: Annotated[list[str] | None, Query()] = None):
    query_items = {"q": q}
    return query_items

@router.post('/')
async def read_item(request: Request):
    return {
        "headers": request.headers,
        "cookies": request.cookies,
        "body": await request.body()
    }


class Item(BaseModel):
    name: str | None = Field(default=None)
    description: str | None = 'test'
    price: float
    tax: float | None

class User(BaseModel):
    username: str
    full_name: str | None = None

@router.put('/items/{item_id}')
async def update_item(item_id: int, item: Item, user: User, file: Annotated[bytes, File()]):
    results = {"item_id": item_id, "item": item, "user": user}
    return results