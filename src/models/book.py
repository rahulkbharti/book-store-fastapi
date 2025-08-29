from sqlalchemy import Column, Integer, String
from src.database.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True, nullable=False)
    author = Column(String, index=True, nullable=False)
    published_year = Column(Integer, nullable=True)
    price = Column(Integer, nullable=True)