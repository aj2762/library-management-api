from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import BookDB

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create the tables on startup if they do not exist yet.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Library Management API",
    description="A simple API for managing library books.",
    version="1.0.0",
)


# ---------- Models ----------

class BookCreate(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    publication_year: int | None = None
    publisher: str | None = None


class BookPatch(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    author: str | None = Field(default=None, min_length=1)
    publication_year: int | None = None
    publisher: str | None = None

    @field_validator("title", "author")
    @classmethod
    def not_null(cls, value):
        # title and author may be omitted, but cannot be explicitly set to null.
        if value is None:
            raise ValueError("This field cannot be null")
        return value


class Book(BookCreate):
    model_config = ConfigDict(from_attributes=True)  # allow reading from DB objects

    id: int


# ---------- Helpers ----------

def get_book_or_404(book_id: int, db: Session) -> BookDB:
    book = db.get(BookDB, book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


# ---------- Routes ----------

@app.get("/books", response_model=list[Book], tags=["Books"])
def get_books(db: Session = Depends(get_db)):
    """Return all books."""
    return db.scalars(select(BookDB).order_by(BookDB.id)).all()


@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED, tags=["Books"])
def add_book(book: BookCreate, db: Session = Depends(get_db)):
    """Add a new book."""
    new_book = BookDB(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@app.get("/books/{book_id}", response_model=Book, tags=["Books"])
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Get one book by its ID."""
    return get_book_or_404(book_id, db)


@app.patch("/books/{book_id}", response_model=Book, tags=["Books"])
def update_book(book_id: int, changes: BookPatch, db: Session = Depends(get_db)):
    """Update only the fields supplied by the user."""
    book = get_book_or_404(book_id, db)
    for field, value in changes.model_dump(exclude_unset=True).items():
        setattr(book, field, value)
    db.commit()
    db.refresh(book)
    return book


@app.delete("/books/{book_id}", tags=["Books"])
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Delete one book by its ID."""
    book = get_book_or_404(book_id, db)
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}
