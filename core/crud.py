from os import name
from sqlalchemy.orm import Session

from . import models, schemas

from passlib.context import CryptContext

pass_manager = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()


def creat_user(db: Session, user: schemas.User_create):
    hashed_password = pass_manager.hash(user.password)
    db_user = models.User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_book_by_id(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_book_by_name(db: Session, name: str):
    return db.query(models.Book).filter(models.Book.name == name).first()


def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Book).offset(skip).limit(limit).all()


def creat_book(db: Session, book: schemas.Book_create, user_id: int):
    db_book = models.Book(
        name=book.name, description=book.description, renter_id=user_id)
    # db_book= models.Book(**book.dict(),renter_id=user_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
