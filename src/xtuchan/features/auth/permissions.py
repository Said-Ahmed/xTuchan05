from typing import List
from fastapi.params import Depends
from starlette import status
from starlette.exceptions import HTTPException

from src.xtuchan.features.auth.dependencies import get_current_user
from src.xtuchan.pydantic_doc import User


class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)):
        if current_user.role in self.allowed_roles or current_user.is_admin:
            return True

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='У вас нет прав на выполнение этого действия'
        )
