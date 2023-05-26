from typing import Optional 

from pydantic import BaseModel


class CollaborationBidBase(BaseModel):
    description: Optional[str] = None


class CollaborationBidCreate(CollaborationBidBase):
    pass


class CollaborationBidUpdate(CollaborationBidBase):
    pass


class CollaborationBidInDBBase(CollaborationBidBase):
    id: Optional[int] = None
    collaboration_id: Optional[int] = None
    bidder_id: Optional[int] = None

    class Config:
        orm_mode = True


class CollaborationBid(CollaborationBidInDBBase):
    pass


class CollaborationBidInDB(CollaborationBidInDBBase):
    pass
