from typing import Optional 
from datetime import datetime

from pydantic import BaseModel


class MessageBase(BaseModel):
    content: Optional[str] = None
    timestamp: Optional[datetime] = None


class MessageCreate(MessageBase):
    pass


class MessageUpdate(MessageBase):
    pass


class MessageInDBBase(MessageBase):
    id: Optional[int] = None
    sender_id: Optional[int] = None
    receiver_id: Optional[int] = None

    class Config:
        orm_mode = True


class Message(MessageInDBBase):
    pass


class MessageInDB(MessageInDBBase):
    pass
