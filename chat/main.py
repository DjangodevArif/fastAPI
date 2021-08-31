
from fastapi import FastAPI
from routers.users import users
from routers.chat import chat
from database import engine, Base
# from . import base


app = FastAPI()

app.include_router(users.router, prefix="/user")
app.include_router(chat.router, prefix="/chat")

# userModel.Base.metadata.create_all(bind=engine)
# chatModel.Base.metadata.create_all(bind=engine)
