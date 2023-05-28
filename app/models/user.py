from sqlalchemy import Boolean, Column, Integer, String, Float, CheckConstraint
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.utils.languages import LANGUGAGE_MAP


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=False, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_superuser = Column(Boolean, default=False)
    prefered_language = Column(String, nullable=True)
    country = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)

    # organization fields
    organization_name = Column(String, nullable=True)
    organization_description = Column(String, nullable=True)
    organization_rating = Column(Float, nullable=True, default=-1)
    
    problems = relationship("Problem", back_populates="owner")
    problembids = relationship("ProblemBid", back_populates="bidder")

    collaborations = relationship("Collaboration", back_populates="owner")
    collaborationrequets = relationship("CollaborationRequest", back_populates="requester")
    
    sent_messages = relationship("Message", back_populates="sender", foreign_keys="Message.sender_id")
    received_messages = relationship("Message", back_populates="receiver", foreign_keys="Message.receiver_id")


    __table_args__ = (
        CheckConstraint(prefered_language.in_(LANGUGAGE_MAP), name='prefered_language_check'),
    )
