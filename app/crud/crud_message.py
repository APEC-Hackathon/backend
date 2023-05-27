from typing import List 

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.message import Message
from app.models.user import User
from app.schemas.message import MessageCreate, MessageUpdate
from app.utils.translation import translate


class CRUDMessage(CRUDBase[Message, MessageCreate, MessageUpdate]):
    def create_with_sender_and_receiver(
        self, db: Session, *, obj_in: MessageCreate, sender_id: int, receiver_id: int 
    ) -> Message:
        obj_in_data = jsonable_encoder(obj_in)
        receiver_prefered_language = db.query(User.prefered_language).filter(User.id == receiver_id).first()
        print(receiver_prefered_language[0])
        translated_content = translate(obj_in_data['content'], receiver_prefered_language[0])
        db_obj = self.model(**obj_in_data, sender_id=sender_id, receiver_id=receiver_id, translated_content=translated_content)
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
