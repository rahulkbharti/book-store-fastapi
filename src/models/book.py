from sqlalchemy import Column, Integer, String
from src.database.db import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    published_year = Column(Integer)
    price = Column(Integer)