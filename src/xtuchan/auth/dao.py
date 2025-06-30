from xtuchan.dao.base import BaseDAO
from xtuchan.auth.models import Users


class UsersDAO(BaseDAO):
    model = Users