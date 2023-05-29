from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class ProblemBid(Base):
    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problem.id"))
    problem = relationship("Problem", back_populates="bids")
    bidder_id = Column(Integer, ForeignKey("user.id"))
    bidder = relationship("User", back_populates="problembids")
    description = Column(String, nullable=True)
