from typing import Optional

from pydantic import BaseModel


class ProblemBidBase(BaseModel):
    description: Optional[str] = None


class ProblemBidCreate(ProblemBidBase):
    pass


class ProblemBidUpdate(ProblemBidBase):
    pass


class ProblemBidInDBBase(ProblemBidBase):
    id: Optional[int] = None
    problem_id: Optional[int] = None
    bidder_id: Optional[int] = None

    class Config:
        orm_mode = True


class ProblemBid(ProblemBidInDBBase):
    pass 


class ProblemBidInDB(ProblemBidInDBBase):
    pass
