from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    title = Column(String, default="My Portfolio")
    tagline = Column(Text, nullable=True)
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="portfolio")
    # one portfolio has many projects
    projects = relationship("Project", back_populates="portfolio", cascade="all, delete-orphan")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"))
    repo_name = Column(String)
    repo_url = Column(String)
    language = Column(String, nullable=True)
    ai_description = Column(Text, nullable=True)
    display_order = Column(Integer, default=0)
    is_featured = Column(Boolean, default=True)

    # each project belongs to one portfolio
    portfolio = relationship("Portfolio", back_populates="projects")