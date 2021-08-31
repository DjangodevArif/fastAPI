
from typing import List
from fastapi.param_functions import Depends
from sqlalchemy.sql.elements import or_
from routers.chat.schemas import PrivateChatRoomRes
from routers.chat.models import PrivateChatRoom
from routers.users.models import User
from sqlalchemy.orm.session import Session


def createChatRoom(db: Session, user1: int, user2: int):
    db_Room = PrivateChatRoom(user1=user1, user2=user2)
    db.add(db_Room)
    db.commit()
    db.refresh(db_Room)
    return db_Room


def getRoombyUser(db: Session, user_1: int, user_2: int):
    # may_1 = db.query(PrivateChatRoom).get({"user1": user_1, "user2": user_2})
    may_1 = db.query(PrivateChatRoom).filter(
        PrivateChatRoom.user1 == user_1, PrivateChatRoom.user2 == user_2).first()
    if may_1:
        return may_1
    return db.query(PrivateChatRoom).filter(PrivateChatRoom.user1 == user_2, PrivateChatRoom.user2 == user_1).first()


def getRoombyId(db: Session, id: int):
    return db.query(PrivateChatRoom).get(id)


def roomActiveorDeactive(db: Session, user_1: int, user_2: int):
    room = getRoombyUser(db, user_1, user_2)
    room.is_active = not room.is_active
    db.commit()
    return room


def getUserRooms(db: Session, user: User):
    rooms = db.query(PrivateChatRoom).filter(
        or_(PrivateChatRoom.user1 == user.id, PrivateChatRoom.user2 == user.id), PrivateChatRoom.is_active == True).all()
    return rooms


def getFriends(db: Session, user: User):
    rooms = getUserRooms(db, user)
    friendlist = []
    for user in rooms:
        if user.user1 == user.id:
            friendlist.append(user.user2)
        else:
            friendlist.append(user.user1)
    friends = db.query(User).filter(User.id.in_(friendlist)).all()
    return friends
