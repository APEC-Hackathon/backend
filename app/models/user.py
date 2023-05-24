from sqlalchemy import Boolean, Column, Integer, String, Float
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=False, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_superuser = Column(Boolean, default=False)

    # organization fields
    organization_name = Column(String, nullable=True)
    organization_description = Column(String, nullable=True)
    organization_rating = Column(Float, nullable=True, default=-1)
    
    problems = relationship("Problem", back_populates="owner")
    collaborations = relationship("Collaboration", back_populates="owner")
