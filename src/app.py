from fastapi import FastAPI , Depends
from src.routes import book, user, auth
from src.database.db import engine
from src.models.user import Base as UserBase
from src.models.book import Base as BookBase

# Create database tables
UserBase.metadata.create_all(bind=engine)
BookBase.metadata.create_all(bind=engine)

app = FastAPI(
    title="Book Store API",
    description="API for managing a book store",
    version="1.0.0"
)
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(book.router, prefix="/books", tags=["books"])
app.include_router(user.router, prefix="/users", tags=["users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Book Store API"}

