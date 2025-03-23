from app.dao.base import BaseDAO
from app.reviews.models import Review


class ReviewDao(BaseDAO):
    model = Review