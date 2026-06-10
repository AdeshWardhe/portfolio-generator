from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.services.github import fetch_github_repos, fetch_github_user
from app.models.user import User

router = APIRouter(prefix="/repos", tags=["repos"])

@router.get("/")
async def get_repos(current_user: User = Depends(get_current_user)):
    """
    Fetch all GitHub repos of the logged in user.
    Requires JWT token in the Authorization header.
    """
    github_token = current_user.github_access_token

    if not github_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="GitHub access token missing. Please reconnect GitHub."
        )

    try:
        # fetch repos from GitHub API
        repos = await fetch_github_repos(github_token)

        # fetch user profile too
        github_profile = await fetch_github_user(github_token)

        # clean up the data we return
        cleaned_repos = [
            {
                "id": r["id"],
                "name": r["name"],
                "description": r["description"],
                "language": r["language"],
                "stars": r["stargazers_count"],
                "forks": r["forks_count"],
                "url": r["html_url"],
                "topics": r.get("topics", []),
                "updated_at": r["updated_at"]
            }
            for r in repos
        ]

        return {
            "profile": {
                "username": github_profile["login"],
                "name": github_profile.get("name"),
                "bio": github_profile.get("bio"),
                "avatar_url": github_profile["avatar_url"],
                "followers": github_profile["followers"],
                "public_repos": github_profile["public_repos"],
                "github_url": github_profile["html_url"]
            },
            "repos": cleaned_repos,
            "total": len(cleaned_repos)
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Failed to fetch GitHub data: {str(e)}"
        )