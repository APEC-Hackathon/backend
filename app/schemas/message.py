from typing import Optional 
from datetime import datetime

from pydantic import BaseModel


class MessageBase(BaseModel):
    content: Optional[str] = None


class MessageCreate(MessageBase):
    pass


class MessageUpdate(MessageBase):
    pass


class MessageInDBBase(MessageBase):
    id: Optional[int] = None
    translated_content: Optional[str] = None
    sender_id: Optional[int] = None
    receiver_id: Optional[int] = None
    timestamp: Optional[datetime] = None

    class Config:
        orm_mode = True


class Message(MessageInDBBase):
    pass


class MessageInDB(MessageInDBBase):
    pass
