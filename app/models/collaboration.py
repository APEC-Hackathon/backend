from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Collaboration(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="collaborations")
    image_url = Column(String, nullable=True)

    source_id = Column(Integer, ForeignKey("problem.id"))
    source = relationship("Problem", back_populates="alliances")
    bids = relationship("CollaborationBid", back_populates="collaboration")


class CollaborationBid(Base):
    id = Column(Integer, primary_key=True, index=True)
    collaboration_id = Column(Integer, ForeignKey("collaboration.id"))
    collaboration = relationship("Collaboration", back_populates="bids")
    bidder_id = Column(Integer, ForeignKey("user.id"))
    bidder = relationship("User", back_populates="collaborationbids")
    description = Column(String, nullable=True)
