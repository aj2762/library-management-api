# Library Management API

A beginner-friendly REST API for managing library books, built with FastAPI.

## Features

- `GET /books` — list all books
- `POST /books` — add a book
- `GET /books/{book_id}` — get a book by ID
- `PATCH /books/{book_id}` — update selected fields of a book
- `DELETE /books/{book_id}` — delete a book by ID

## Technologies

- Python 3.10+
- FastAPI
- Pydantic
- Uvicorn

## Setup (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

Open http://127.0.0.1:8000/docs to try the API.

## Example: Add a book

Send a `POST` request to `/books` with this JSON body:

```json
{
  "title": "The Little Prince",
  "author": "Antoine de Saint-Exupery",
  "publication_year": 1943,
  "publisher": "Reynal & Hitchcock"
}
```

## Example: Update only the title

Send a `PATCH` request to `/books/1`:

```json
{
  "title": "The Little Prince - Updated Edition"
}
```

## Data storage

Books are stored in a Python dictionary in memory. No database is used. Data is cleared when the application stops or restarts.
