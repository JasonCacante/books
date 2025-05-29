from fastapi import Body, FastAPI

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
async def create_book(book=Body()):
    BOOKS.append(book)
    return {"message": "Book created successfully", "book": book}
