from typing import List 

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.collaboration_request import CollaborationRequest
from app.schemas.collaboration_request import CollaborationRequestCreate, CollaborationRequestUpdate


class CRUDCollaborationBid(CRUDBase[CollaborationRequest, CollaborationRequestCreate, CollaborationRequestUpdate]):
    def create_with_requester(
        self, db: Session, *, obj_in: CollaborationRequestCreate, requester_id: int
    ) -> CollaborationRequest:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, requester_id=requester_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_multi_by_requester(
        self, db: Session, *, requester_id: int, skip: int = 0, limit: int = 100
    ) -> List[CollaborationRequest]:
        return (
            db.query(self.model)
            .filter(CollaborationRequest.requester_id == requester_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_multi_by_collaboration(
        self, db: Session, *, collaboration_id: int, skip: int = 0, limit: int = 100
    ) -> List[CollaborationRequest]:
        return (
            db.query(self.model)
            .filter(CollaborationRequest.collaboration_id == collaboration_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def accept(
        self, db: Session, *, collaboration_request_id: int
    ) -> CollaborationRequest:
        db_obj = db.query(self.model).filter(CollaborationRequest.id == collaboration_request_id).first()
        db_obj.status = "accepted"
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def reject(
        self, db: Session, *, collaboration_request_id: int
    ) -> CollaborationRequest:
        db_obj = db.query(self.model).filter(CollaborationRequest.id == collaboration_request_id).first()
        db_obj.status = "rejected"
        db.commit()
        db.refresh(db_obj)
        return db_obj
    

collaboration_request = CRUDCollaborationBid(CollaborationRequest)
