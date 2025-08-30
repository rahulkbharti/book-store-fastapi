from fastapi import APIRouter, Depends, Request, HTTPException, status , Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from src.database.database import get_async_db
from src.models.book import Book
from src.schemas.book import BookResponse, BookCreate, BookUpdate, PaginatedBookResponse,PaginationInfo
from src.middlewares.auth import protected_route

from typing import Optional

router = APIRouter()


@router.get("/", response_model=PaginatedBookResponse, status_code=status.HTTP_200_OK)
async def get_books(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    author: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Get paginated list of books with optional author filter (partial match).
    """
    offset = (page - 1) * limit

    # Build base query
    base_query = select(Book).order_by(Book.id)
    count_query = select(func.count(Book.id))
    
    # Apply author filter if provided - partial match using ilike
    if author:
        author_filter = f"%{author}%"
        base_query = base_query.where(Book.author.ilike(author_filter))
        count_query = count_query.where(Book.author.ilike(author_filter))

    # Execute paginated query
    paginated_query = base_query.offset(offset).limit(limit)
    result = await db.execute(paginated_query)
    books = result.scalars().all()
    
    # Convert to Pydantic models
    book_responses = [BookResponse.model_validate(book) for book in books]
    
    # Get total count
    count_result = await db.execute(count_query)
    total_books = count_result.scalar_one()
    
    # Calculate pagination info
    total_pages = (total_books + limit - 1) // limit if total_books > 0 else 1
    
    return PaginatedBookResponse(
        data=book_responses,
        pagination=PaginationInfo(
            page=page,
            limit=limit,
            total_items=total_books,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_prev=page > 1
        )
    )

@router.get("/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
async def get_book(book_id: int, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()
    
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return book

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
@protected_route
async def create_book(request: Request, book: BookCreate, db: AsyncSession = Depends(get_async_db)):
    db_book = Book(**book.model_dump())
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book

@router.put("/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
@protected_route
async def update_book(request: Request, book_id: int, book: BookUpdate, db: AsyncSession = Depends(get_async_db)):
    # Get the book first
    result = await db.execute(select(Book).where(Book.id == book_id))
    db_book = result.scalar_one_or_none()
    
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    # Exclude None values (fields that weren't provided)
    update_data = book.model_dump(exclude_none=True)
    
    for key, value in update_data.items():
        setattr(db_book, key, value)
    
    await db.commit()
    await db.refresh(db_book)
    return db_book

@router.delete("/{book_id}", response_model=dict, status_code=status.HTTP_200_OK)
@protected_route
async def delete_book(request: Request, book_id: int, db: AsyncSession = Depends(get_async_db)):
    # Get the book first
    result = await db.execute(select(Book).where(Book.id == book_id))
    db_book = result.scalar_one_or_none()
    
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    await db.delete(db_book)
    await db.commit()
    return {"message": "Book deleted successfully"}