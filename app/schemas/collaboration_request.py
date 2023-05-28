from typing import Optional 

from pydantic import BaseModel


class CollaborationRequestBase(BaseModel):
    description: Optional[str] = None


class CollaborationRequestCreate(CollaborationRequestBase):
    collaboration_id: int = None


class CollaborationRequestUpdate(CollaborationRequestBase):
    pass


class CollaborationRequestInDBBase(CollaborationRequestBase):
    id: Optional[int] = None
    collaboration_id: Optional[int] = None
    requester_id: Optional[int] = None
    status: Optional[str] = None

    class Config:
        orm_mode = True


class CollaborationRequest(CollaborationRequestInDBBase):
    pass


class CollaborationRequestInDB(CollaborationRequestInDBBase):
    pass
