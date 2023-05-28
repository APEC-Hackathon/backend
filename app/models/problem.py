from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Problem(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="problems")
    bid_deadline = Column(DateTime, nullable=True)
    image_url = Column(String, nullable=True)

    alliances = relationship("Collaboration", back_populates="source")
    bids = relationship("ProblemBid", back_populates="problem")


class ProblemBid(Base):
    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problem.id"))
    problem = relationship("Problem", back_populates="bids")
    bidder_id = Column(Integer, ForeignKey("user.id"))
    bidder = relationship("User", back_populates="problembids")
    description = Column(String, nullable=True)
