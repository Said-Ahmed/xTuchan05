from src.xtuchan.features.dao.base import BaseDAO
from src.xtuchan.features.auth.models import Users


class UsersDAO(BaseDAO):
    model = Users