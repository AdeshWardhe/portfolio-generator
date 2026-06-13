from pydantic import BaseModel
from typing import List, Optional

class ProjectInput(BaseModel):
    repo_name: str
    repo_url: str
    language: Optional[str] = None
    ai_description: Optional[str] = None
    display_order: int = 0

class PortfolioSaveRequest(BaseModel):
    title: str
    tagline: Optional[str] = None
    projects: List[ProjectInput]

class ProjectResponse(BaseModel):
    repo_name: str
    repo_url: str
    language: Optional[str] = None
    ai_description: Optional[str] = None
    display_order: int

    class Config:
        from_attributes = True

class PortfolioResponse(BaseModel):
    title: str
    tagline: Optional[str] = None
    is_published: bool
    projects: List[ProjectResponse]

    class Config:
        from_attributes = True