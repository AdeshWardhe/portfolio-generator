from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.services.auth import create_access_token
from app.services.github import exchange_code_for_token, fetch_github_user
from os import getenv

router = APIRouter(prefix="/auth", tags=["auth"])

GITHUB_CLIENT_ID = getenv("GITHUB_CLIENT_ID")

@router.get("/github/login")
def github_login():
    """Step 1: Redirect user to GitHub login page."""
    github_auth_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={GITHUB_CLIENT_ID}"
        f"&scope=read:user,repo"
    )
    return {"url": github_auth_url}

@router.get("/github/callback")
async def github_callback(code: str, db: Session = Depends(get_db)):
    """
    Step 2: GitHub redirects back here with a code.
    We exchange the code for an access token,
    fetch the user's GitHub profile,
    create or update the user in our database,
    and return a JWT token.
    """
    # exchange code for github token
    github_token = await exchange_code_for_token(code)
    if not github_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to get GitHub token"
        )

    # fetch github profile
    github_user = await fetch_github_user(github_token)

    # check if user already exists in our database
    user = db.query(User).filter(
        User.github_username == github_user["login"]
    ).first()

    if not user:
        # create new user
        user = User(
            username=github_user["login"],
            email=github_user.get("email") or f"{github_user['login']}@github.com",
            hashed_password="",
            github_username=github_user["login"],
            github_access_token=github_token,
            bio=github_user.get("bio"),
            avatar_url=github_user.get("avatar_url")
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        # update existing user's token and info
        user.github_access_token = github_token
        user.bio = github_user.get("bio")
        user.avatar_url = github_user.get("avatar_url")
        db.commit()
        db.refresh(user)

    # create JWT token for our app
    jwt_token = create_access_token(data={
        "user_id": user.id,
        "username": user.username,
        "github_username": user.github_username
    })

    # redirect to dashboard with token in URL
    from fastapi.responses import RedirectResponse
    redirect_url = f"/dashboard.html?token={jwt_token}"
    return RedirectResponse(url=redirect_url)

@router.get("/me")
async def get_me(db: Session = Depends(get_db)):
    """Test endpoint — returns a message."""
    return {"message": "Auth is working!"}