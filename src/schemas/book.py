from pydantic import BaseModel
from typing import Optional,List

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
    
    class ConfigDict:
        from_attributes = True
    
class PaginationInfo(BaseModel):
    page: int
    limit: int
    total_items: int
    total_pages: int
    has_next: bool
    has_prev: bool

class PaginatedBookResponse(BaseModel):
    data: List[BookResponse]
    pagination: PaginationInfo

    class ConfigDict:
        from_attributes = True