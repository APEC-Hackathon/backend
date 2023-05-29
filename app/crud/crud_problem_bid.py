from typing import List 

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.problem_bid import ProblemBid
from app.schemas.problem_bid import ProblemBidCreate, ProblemBidUpdate


class CRUDProblemBid(CRUDBase[ProblemBid, ProblemBidCreate, ProblemBidUpdate]):
    def create_with_bidder(
        self, db: Session, *, obj_in: ProblemBidCreate, bidder_id: int
    ) -> ProblemBid:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, bidder_id=bidder_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_multi_by_bidder(
        self, db: Session, *, bidder_id: int, skip: int = 0, limit: int = 100
    ) -> List[ProblemBid]:
        return (
            db.query(self.model)
            .filter(ProblemBid.bidder_id == bidder_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_multi_by_problem(
        self, db: Session, *, problem_id: int, skip: int = 0, limit: int = 100
    ) -> List[ProblemBid]:
        return (
            db.query(self.model)
            .filter(ProblemBid.problem_id == problem_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    

problem_bid = CRUDProblemBid(ProblemBid)
