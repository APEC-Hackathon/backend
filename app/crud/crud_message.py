from typing import List 

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.message import Message
from app.schemas.message import MessageCreate, MessageUpdate


class CRUDMessage(CRUDBase[Message, MessageCreate, MessageUpdate]):
    def create_with_sender_and_receiver(
        self, db: Session, *, obj_in: MessageCreate, sender_id: int, receiver_id: int 
    ) -> Message:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, sender_id=sender_id, receiver_id=receiver_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_multi_by_sender_and_receiver(
        self, db: Session, *, receiver_id: int, sender_id: int, skip: int = 0, limit: int = 100
    ) -> List[Message]:
        return (
            db.query(self.model)
            .filter(Message.receiver_id == receiver_id)
            .filter(Message.sender_id == sender_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


message = CRUDMessage(Message)
