from routers.users.schemas import UserRes
from starlette.responses import JSONResponse
from typing import List
from routers.chat.uttils import createChatRoom, getRoombyUser, roomActiveorDeactive, getFriends
from routers.users.crud import getUserbyToken, get_user_by_data
from dependencies import getAuthenticity, get_db
from fastapi import APIRouter, HTTPException, status, Response
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session

router = APIRouter(tags=["Chat"])


@router.get("/add/{user_id}")
async def addOrRemoveFriend(user_id: int, token: str = Depends(getAuthenticity), db: Session = Depends(get_db)):
    current_user = getUserbyToken(db, token)
    other_user = get_user_by_data(db, id=user_id)
    exist = getRoombyUser(db, user_1=current_user.id, user_2=user_id)
    if exist:
        activeOrDeactive = roomActiveorDeactive(
            db, user_1=current_user.id, user_2=user_id)
        message = f"Friendship with {other_user.username} is deactivate !"
        if activeOrDeactive.is_active == True:
            message = f"Friendship with {other_user.username} is activate !"
        return JSONResponse(content={'Message': message}, status_code=status.HTTP_202_ACCEPTED)
    room = createChatRoom(db, user1=current_user.id, user2=user_id)
    return JSONResponse(content={'Message': f'"{other_user.username}" is added in your friend list !', }, status_code=status.HTTP_201_CREATED)


@router.get("/friend-list", response_model=List[UserRes])
async def getFriendList(db: Session = Depends(get_db), token: str = Depends(getAuthenticity)):
    user = getUserbyToken(db, token)
    friends = getFriends(db, user)
    return friends
