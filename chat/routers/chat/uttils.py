
from routers.chat.models import PrivateChatRoom
from sqlalchemy.orm.session import Session


def createChatRoom(db: Session, user1: int, user2: int):
    db_Room = PrivateChatRoom(user1=user1, user2=user2)
    db.add(db_Room)
    db.commit()
    db.refresh(db_Room)
    return db_Room


def getRoombyUser(db: Session, user_1: int, user_2: int):
    may_1 = db.query(PrivateChatRoom).get({"user1": user_1, "user2": user_2})
    if may_1:
        return may_1
    return db.query(PrivateChatRoom).get({"user1": user_2, "user2": user_2})


def getRoombyId(db: Session, id: int):
    return db.query(PrivateChatRoom).get(id)
