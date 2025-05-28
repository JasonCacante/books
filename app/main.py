from fastapi import Body, FastAPI

app = FastAPI()


BOOKS = [
    {"title": "Book One", "author": "Author A", "category": "science"},
    {"title": "Book Two", "author": "Author B", "category": "fiction"},
    {"title": "Book Three", "author": "Author C", "category": "history"},
    {"title": "Book Four", "author": "Author D", "category": "science"},
    {"title": "Book Five", "author": "Author E", "category": "fiction"},
    {"title": "Book Six", "author": "Author F", "category": "history"},
    {"title": "Book Seven", "author": "Author G", "category": "science"},
    {"title": "Book Eight", "author": "Author H", "category": "fiction"},
    {"title": "Book Nine", "author": "Author I", "category": "history"},
    {"title": "Book Ten", "author": "Author J", "category": "science"},
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book["title"].casefold() == book_title.casefold():
            return book
    return {"error": "Book not found"}


@app.get("/books/category/")
async def read_category_by_query(category: str):
    books_to_return = [
        book for book in BOOKS if book["category"].casefold() == category.casefold()
    ]
    if not books_to_return:
        return {"error": "No books found in this category"}
    return books_to_return


@app.get("/books/{book_author}/")
async def read_books_by_author(book_author: str, category: str):
    books_to_return = [
        book
        for book in BOOKS
        if book["author"].casefold() == book_author.casefold()
        and book["category"].casefold() == category.casefold()
    ]
    if not books_to_return:
        return {"error": "No books found by this author"}
    return books_to_return


@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)
    return {"message": "Book added successfully", "book": new_book}


@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for index, book in enumerate(BOOKS):
        if book["title"].casefold() == updated_book["title"].casefold():
            BOOKS[index] = updated_book
            return {"message": "Book updated successfully", "book": updated_book}
    return {"error": "Book not found for update"}


@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for index, book in enumerate(BOOKS):
        if book["title"].casefold() == book_title.casefold():
            del BOOKS[index]
            return {"message": "Book deleted successfully"}
    return {"error": "Book not found for deletion"}
