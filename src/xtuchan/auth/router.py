from fastapi import APIRouter, Response
from fastapi.params import Depends

from xtuchan.auth.auth import get_password_hash, authenticate_user, create_access_token
from xtuchan.auth.dao import UsersDAO
from xtuchan.auth.dependencies import get_current_user
from xtuchan.auth.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from xtuchan.auth.models import Users
from xtuchan.auth.schemas import SUserAuth, SUserRegister

router = APIRouter(
    prefix='/auth',
    tags=['Auth $ Пользователи'],
)


@router.post('/register')
async def register_user(user_data: SUserRegister):
    user = await UsersDAO.find_one_or_none(email = user_data.email)

    if user:
        raise UserAlreadyExistsException

    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password, is_admin=user_data.is_admin)


@router.post('/login')
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)

    if not user:
        raise IncorrectEmailOrPasswordException

    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie('tuchan_access_token', access_token, httponly=True)

    return {'tuchan_access_token': access_token, 'is_admin': user.is_admin}


@router.post('/logout')
async def logout_user(response: Response):
    response.delete_cookie('tuchan_access_token')


@router.get('/me')
async def get_current_user(current_user: Users = Depends(get_current_user)):
    return current_user


