from typing import List 

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.collaboration import CollaborationRequest
from app.schemas.collaboration_request import CollaborationRequestCreate, CollaborationRequestUpdate


class CRUDCollaborationBid(CRUDBase[CollaborationRequest, CollaborationRequestCreate, CollaborationRequestUpdate]):
    def create_with_requester(
        self, db: Session, *, obj_in: CollaborationRequestCreate, bidder_id: int
    ) -> CollaborationRequest:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, bidder_id=bidder_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_multi_by_requester(
        self, db: Session, *, bidder_id: int, skip: int = 0, limit: int = 100
    ) -> List[CollaborationRequest]:
        return (
            db.query(self.model)
            .filter(CollaborationRequest.bidder_id == bidder_id)
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
    

collaboration_request = CRUDCollaborationBid(CollaborationRequest)
