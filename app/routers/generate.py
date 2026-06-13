from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from app.dependencies import get_current_user
from app.services.ai import generate_project_description
from app.models.user import User

router = APIRouter(prefix="/generate", tags=["generate"])

class GenerateRequest(BaseModel):
    repo_name: str
    language: Optional[str] = None
    topics: List[str] = []
    existing_description: Optional[str] = None

@router.post("/description")
async def generate_description(
    body: GenerateRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Generate an AI-written project description for a repo.
    Requires JWT token — only logged-in users can use this.
    """
    try:
        description = await generate_project_description(
            repo_name=body.repo_name,
            language=body.language,
            topics=body.topics,
            existing_description=body.existing_description
        )
        return {"description": description}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AI generation failed: {str(e)}"
        )