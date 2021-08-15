from typing import List

from fastapi import Depends, FastAPI, HTTPException, status, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users", response_model=List[schemas.User_res])
def read_user(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip, limit)
    return users


@app.get("/books", response_model=List[schemas.Book_res])
def read_book(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip, limit)
    return books


@app.post("/users", response_model=schemas.User_res)
def save_user(user: schemas.User_create, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            "Username already exist !")
    return crud.creat_user(db, user)


@app.post("/users/{user_id}/book", response_model=schemas.Book_res)
def save_book(book: schemas.Book_create, user_id: int, db: Session = Depends(get_db)):
    return crud.creat_book(db, book, user_id)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(data)
