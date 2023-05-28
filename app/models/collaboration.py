from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
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
    requests = relationship("CollaborationRequest", back_populates="collaboration")


class CollaborationRequest(Base):
    id = Column(Integer, primary_key=True, index=True)
    collaboration_id = Column(Integer, ForeignKey("collaboration.id"))
    collaboration = relationship("Collaboration", back_populates="requests")
    requester_id = Column(Integer, ForeignKey("user.id"))
    requester = relationship("User", back_populates="collaborationrequets")
    description = Column(String, nullable=True)
    status = Column(String, nullable=False, default="pending")

    __table_args__ = (
        CheckConstraint(status.in_(["pending", "accepted", "rejected"]), name='state_check'),
    )
