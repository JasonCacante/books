from fastapi import FastAPI

app = FastAPI()


@app.get("/books")
async def read_all_books():
    return {"message": "Hello from FastAPI with Docker, Postgres, and Redis!"}
