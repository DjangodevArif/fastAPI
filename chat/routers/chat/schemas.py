from ..users.schemas import UserRes
from typing import List
from pydantic import BaseModel


class PrivateChatRoomCreate(BaseModel):
    user1: int
    user2: int
    connected_user: List(UserRes)


class PrivateChatRoomRes(PrivateChatRoomCreate):
    id: int
    is_active: bool

    class config:
        orm_mode = True
