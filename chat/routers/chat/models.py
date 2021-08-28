from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, Integer, String
# from ...database import Base


class PrivateChatRoom(Base):
    __tablename__ = "privatechatroom"
    id = Column(Integer, primary_key=True, index=True)
    user1 = Column(Integer, ForeignKey("users.id"))
    user2 = Column(Integer, ForeignKey("users.id"))
    is_active = Column(Boolean, default=True)
