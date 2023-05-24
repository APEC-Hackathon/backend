from typing import Optional 
from datetime import datetime

from pydantic import BaseModel


class ProblemBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    bid_deadline: Optional[datetime] = None


class ProblemCreate(ProblemBase):
    pass


class ProblemUpdate(ProblemBase):
    pass 


class ProblemInDBBase(ProblemBase):
    id: Optional[int] = None
    owner_id: Optional[int] = None

    class Config:
        orm_mode = True


class Problem(ProblemInDBBase):
    pass


class ProblemInDB(ProblemInDBBase):
    pass

