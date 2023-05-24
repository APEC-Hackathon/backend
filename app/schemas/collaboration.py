from typing import Optional 

from pydantic import BaseModel


class CollaborationBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    source_id: Optional[int] = None


class CollaborationCreate(CollaborationBase):
    pass


class CollaborationUpdate(CollaborationBase):
    pass 


class CollaborationInDBBase(CollaborationBase):
    id: Optional[int] = None
    owner_id: Optional[int] = None

    class Config:
        orm_mode = True


class Collaboration(CollaborationInDBBase):
    pass


class CollaborationInDB(CollaborationInDBBase):
    pass
