from src.xtuchan.features.dao.base import BaseDAO
from src.xtuchan.features.reviews.models import Review


class ReviewDao(BaseDAO):
    model = Review