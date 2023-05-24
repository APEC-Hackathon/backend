from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_superuser = Column(Boolean, default=False)

    # organization fields
    organization_name = Column(String, nullable=True)
    organization_description = Column(String, nullable=True)
    organization_rating = Column(Integer, nullable=True, default=-1)
