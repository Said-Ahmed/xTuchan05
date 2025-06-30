from xtuchan.dao.base import BaseDAO
from xtuchan.reviews.models import Review


class ReviewDao(BaseDAO):
    model = Review