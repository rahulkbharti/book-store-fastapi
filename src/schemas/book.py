from pydantic import BaseModel
from typing import Optional

# Book Schemas
class BookBase(BaseModel):
    title: str
    author: str
    published_year: Optional[int] = None
    price: Optional[float] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    published_year: Optional[int] = None
    price: Optional[float] = None

class BookResponse(BookBase):
    id: int