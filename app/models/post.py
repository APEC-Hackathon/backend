from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Post(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    # relationship to organization


class Problem(Post):
    pass 


class Collaboration(Post):
    target = relationship("Problem", back_populates="alliances")

