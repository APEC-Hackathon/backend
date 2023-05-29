from typing import Optional 
from datetime import datetime

from pydantic import BaseModel, HttpUrl


class ProblemBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    bid_deadline: Optional[datetime] = None
    image_url: Optional[HttpUrl] = None


class ProblemCreate(ProblemBase):
    pass


class ProblemUpdate(ProblemBase):
    bid_winner_id: Optional[int] = None


class ProblemInDBBase(ProblemBase):
    id: Optional[int] = None
    owner_id: Optional[int] = None
    bid_winner_id: Optional[int] = None

    class Config:
        orm_mode = True


class Problem(ProblemInDBBase):
    pass


class ProblemInDB(ProblemInDBBase):
    pass

