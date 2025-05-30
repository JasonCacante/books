from fastapi import Body, FastAPI
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()


class Book:
    book_id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, book_id, title, author, description, rating):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    book_id: Optional[int] = None
    title: str = Field(min_length=3, max_length=100)
    author: str = Field(min_length=3, max_length=100)
    description: str = Field(
        min_length=10, max_length=500, description="A brief description of the book"
    )
    rating: int = Field(ge=1, le=5, description="Rating of the book from 1 to 5")

    # I need to add some kind of validation


BOOKS = [
    Book(1, "1984", "George Orwell", "Dystopian novel set in totalitarian society", 5),
    Book(
        2,
        "To Kill a Mockingbird",
        "Harper Lee",
        "Novel about racial injustice in the Deep South",
        1,
    ),
    Book(
        3,
        "The Great Gatsby",
        "F. Scott Fitzgerald",
        "Story of the mysteriously wealthy Jay Gatsby",
        4,
    ),
    Book(
        4,
        "Pride and Prejudice",
        "Jane Austen",
        "Romantic novel that critiques the British landed gentry",
        5,
    ),
    Book(
        5,
        "Brave New World",
        "Aldous Huxley",
        "Dystopian novel about a technologically advanced future",
        4,
    ),
    Book(
        6,
        "The Catcher in the Rye",
        "J.D. Salinger",
        "Story of teenage angst and alienation",
        4,
    ),
    Book(7, "Fahrenheit 451", "Ray Bradbury", "Dystopian novel about book burning", 5),
    Book(
        8,
        "The Hobbit",
        "J.R.R. Tolkien",
        "Fantasy novel about the adventures of Bilbo Baggins",
        5,
    ),
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.post("/create_book")
async def create_book(book: BookRequest):
    new_book = Book(**book.model_dump())
    new_book = find_book_id(new_book)
    BOOKS.append(new_book)
    return {"message": "Book created successfully", "book": new_book}


def find_book_id(book: Book):
    book.book_id = 1 if len(BOOKS) == 0 else BOOKS[-1].book_id + 1

    return book
