from fastapi import Body, FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()


class Book:
    book_id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, book_id, title, author, description, rating, published_date):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    book_id: Optional[int] = Field(
        description="ID of the book, will be auto-generated if not provided",
        default=None,
    )
    title: str = Field(min_length=3, max_length=100)
    author: str = Field(min_length=3, max_length=100)
    description: str = Field(
        min_length=10, max_length=500, description="A brief description of the book"
    )
    rating: int = Field(ge=1, le=5, description="Rating of the book from 1 to 5")
    published_date: int = Field(
        ge=1800, le=2300, default=2023, description="Year the book was published"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "description": "A story of the mysteriously wealthy Jay Gatsby and his love for the beautiful Daisy Buchanan.",
                "rating": 4,
                "published_date": 1925,
            }
        }
    }


BOOKS = [
    Book(
        1,
        "1984",
        "George Orwell",
        "Dystopian novel set in totalitarian society",
        5,
        1949,
    ),
    Book(
        2,
        "To Kill a Mockingbird",
        "Harper Lee",
        "Novel about racial injustice in the Deep South",
        1,
        1960,
    ),
    Book(
        3,
        "The Great Gatsby",
        "F. Scott Fitzgerald",
        "Story of the mysteriously wealthy Jay Gatsby",
        4,
        1925,
    ),
    Book(
        4,
        "Pride and Prejudice",
        "Jane Austen",
        "Romantic novel that critiques the British landed gentry",
        5,
        1813,
    ),
    Book(
        5,
        "Brave New World",
        "Aldous Huxley",
        "Dystopian novel about a technologically advanced future",
        4,
        1932,
    ),
    Book(
        6,
        "The Catcher in the Rye",
        "J.D. Salinger",
        "Story of teenage angst and alienation",
        4,
        1951,
    ),
    Book(
        7,
        "Fahrenheit 451",
        "Ray Bradbury",
        "Dystopian novel about book burning",
        5,
        1953,
    ),
    Book(
        8,
        "The Hobbit",
        "J.R.R. Tolkien",
        "Fantasy novel about the adventures of Bilbo Baggins",
        5,
        1937,
    ),
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.book_id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(
    book_rating: int = Query(ge=1, le=5, description="Rating of the book from 1 to 5"),
):
    if book_rating < 1 or book_rating > 5:
        return {"message": "Rating must be between 1 and 5"}

    books_by_rating = [book for book in BOOKS if book.rating == book_rating]

    if not books_by_rating:
        return {"message": "No books found with the specified rating"}

    return books_by_rating


@app.post("/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(book: BookRequest):
    new_book = Book(**book.model_dump())
    new_book = find_book_id(new_book)
    BOOKS.append(new_book)
    return {"message": "Book created successfully", "book": new_book}


def find_book_id(book: Book):
    book.book_id = 1 if len(BOOKS) == 0 else BOOKS[-1].book_id + 1

    return book


@app.put("/update_book/{book_id}", status_code=status.HTTP_200_OK)
async def update_book(book_id: int, book: BookRequest):
    for index, existing_book in enumerate(BOOKS):
        if existing_book.book_id == book_id:
            updated_book = Book(**book.model_dump())
            updated_book.book_id = book_id
            BOOKS[index] = updated_book
            return {"message": "Book updated successfully", "book": updated_book}

    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/delete_book/{book_id}", status_code=status.HTTP_200_OK)
async def delete_book(book_id: int = Path(gt=0)):
    for index, book in enumerate(BOOKS):
        if book.book_id == book_id:
            del BOOKS[index]
            return {"message": "Book deleted successfully"}

    raise HTTPException(status_code=404, detail="Book not found")


@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def read_books_by_published_date(published_date: int = Query(ge=1800, le=2300)):
    books_by_year = [book for book in BOOKS if book.published_date == published_date]

    if not books_by_year:
        return {"message": "No books found for the specified year"}

    return books_by_year
