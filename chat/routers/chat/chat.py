from routers.chat.uttils import createChatRoom
from routers.users.crud import getUserbyToken
from dependencies import getAuthenticity, get_db
from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session

router = APIRouter(tags=["Chat"])


@router.get("/add/{user_id}")
async def addFriend(user_id: int, token: str = Depends(getAuthenticity), db: Session = Depends(get_db)):
    current_user = getUserbyToken(db, token)
    job = createChatRoom(db, user1=current_user.id, user2=user_id)
    return job
