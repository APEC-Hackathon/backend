from typing import List 

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.collaboration import CollaborationBid
from app.schemas.collaboration_bid import CollaborationBidCreate, CollaborationBidUpdate


class CRUDCollaborationBid(CRUDBase[CollaborationBid, CollaborationBidCreate, CollaborationBidUpdate]):
    def create_with_bidder(
        self, db: Session, *, obj_in: CollaborationBidCreate, bidder_id: int
    ) -> CollaborationBid:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, bidder_id=bidder_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_multi_by_bidder(
        self, db: Session, *, bidder_id: int, skip: int = 0, limit: int = 100
    ) -> List[CollaborationBid]:
        return (
            db.query(self.model)
            .filter(CollaborationBid.bidder_id == bidder_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_multi_by_collaboration(
        self, db: Session, *, collaboration_id: int, skip: int = 0, limit: int = 100
    ) -> List[CollaborationBid]:
        return (
            db.query(self.model)
            .filter(CollaborationBid.collaboration_id == collaboration_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    

collaboration_bid = CRUDCollaborationBid(CollaborationBid)
