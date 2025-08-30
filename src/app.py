from fastapi import FastAPI
from src.routes import book, user, auth
from src.database.database import engine, init_models
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    print("App starting...")
    yield
    await engine.dispose()
    print("App shutting down...")

app = FastAPI(
    title="Book Store API",
    description="API for managing a book store",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],        # Specific origins or ["*"] for all
    allow_credentials=True,       # Cookies, auth headers
    allow_methods=["*"],          # GET, POST, PUT, DELETE
    allow_headers=["*"],          # Authorization, Content-Type, etc.
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(book.router, prefix="/books", tags=["books"])
app.include_router(user.router, prefix="/users", tags=["users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Book Store API"}

