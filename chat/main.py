
from fastapi import FastAPI
from .routers.users import models, users
from .database import engine


app = FastAPI()

app.include_router(
    users.router,
    prefix="/user",
)

models.Base.metadata.create_all(bind=engine)
