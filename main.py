from itertools import count

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator

app = FastAPI(
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
    id: int


# ---------- Storage (in-memory; data resets when the server stops) ----------

books: dict[int, Book] = {}
id_counter = count(start=1)


def get_book_or_404(book_id: int) -> Book:
    book = books.get(book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


# ---------- Routes ----------

@app.get("/books", response_model=list[Book], tags=["Books"])
def get_books():
    """Return all books."""
    return list(books.values())


@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED, tags=["Books"])
def add_book(book: BookCreate):
    """Add a new book."""
    new_book = Book(id=next(id_counter), **book.model_dump())
    books[new_book.id] = new_book
    return new_book


@app.get("/books/{book_id}", response_model=Book, tags=["Books"])
def get_book(book_id: int):
    """Get one book by its ID."""
    return get_book_or_404(book_id)


@app.patch("/books/{book_id}", response_model=Book, tags=["Books"])
def update_book(book_id: int, changes: BookPatch):
    """Update only the fields supplied by the user."""
    book = get_book_or_404(book_id)
    updated = book.model_copy(update=changes.model_dump(exclude_unset=True))
    books[book_id] = updated
    return updated


@app.delete("/books/{book_id}", tags=["Books"])
def delete_book(book_id: int):
    """Delete one book by its ID."""
    get_book_or_404(book_id)
    del books[book_id]
    return {"message": "Book deleted successfully"}