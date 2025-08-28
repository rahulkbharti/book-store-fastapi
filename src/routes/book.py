from fastapi import APIRouter, Depends, Request, HTTPException


from src.database.db import get_db
from sqlalchemy.orm import Session
from src.models.book import Book
from src.schemas.book import BookResponse , BookCreate, BookUpdate
from src.middlewares.auth import protected_route

router = APIRouter(tags=["books"])


@router.get("/", response_model=list[BookResponse])
def get_books( db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return books

@router.get("/{book_id}", response_model=BookResponse)
def get_book( book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=BookResponse)
@protected_route
def create_book(request: Request, book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.put("/{book_id}", response_model=BookResponse)
@protected_route
def update_book(request: Request, book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Exclude None values (fields that weren't provided)
    update_data = book.model_dump(exclude_none=True)
    for key, value in update_data.items():
        setattr(db_book, key, value)
    
    db.commit()
    db.refresh(db_book)
    return db_book

@router.delete("/{book_id}", response_model=dict)
@protected_route
def delete_book(request: Request, book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return {"message": "Book deleted successfully"}