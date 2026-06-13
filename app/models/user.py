from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    github_username = Column(String, unique=True, nullable=True, index=True)
    github_access_token = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    avatar_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    portfolio = relationship("Portfolio", back_populates="user", uselist=False, cascade="all, delete-orphan")                   