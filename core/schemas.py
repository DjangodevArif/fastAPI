from typing import List, Optional

from pydantic import BaseModel


class Book_create(BaseModel):
    name: str
    description: Optional[str] = None


class Book_res(Book_create):
    id: int
    renter_id: int
    # rent_books: "User_base"  # it's not working (vice-varca)

    class Config:
        orm_mode = True


class User_base(BaseModel):
    username: str


class User_create(User_base):
    password: str


class User_res(User_base):
    id: int
    is_active: bool
    rent_books: List[Book_res] = []

    class Config:
        orm_mode = True
