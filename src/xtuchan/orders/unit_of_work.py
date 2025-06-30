from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.xtuchan.database import DATABASE_URL


class UnitOfWork:
    def __init__(self):
        self.session_maker = sessionmaker(bind=create_engine(DATABASE_URL))

    def __enter__(self):
        self.session = self.session_maker()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.session.rollback()
            self.session.close()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()