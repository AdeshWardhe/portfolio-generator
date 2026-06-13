from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.portfolio import Portfolio, Project
from app.schemas.portfolio import PortfolioSaveRequest, PortfolioResponse

router = APIRouter(prefix="/portfolio", tags=["portfolio"])

@router.post("/save")
def save_portfolio(
    body: PortfolioSaveRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Save (create or update) the logged-in user's portfolio.
    """
    # check if user already has a portfolio
    portfolio = db.query(Portfolio).filter(Portfolio.user_id == current_user.id).first()

    if not portfolio:
        # create new portfolio
        portfolio = Portfolio(
            user_id=current_user.id,
            title=body.title,
            tagline=body.tagline
        )
        db.add(portfolio)
        db.commit()
        db.refresh(portfolio)
    else:
        # update existing portfolio
        portfolio.title = body.title
        portfolio.tagline = body.tagline
        db.commit()

        # delete old projects to replace with new selection
        db.query(Project).filter(Project.portfolio_id == portfolio.id).delete()
        db.commit()

    # create new project rows
    for project_data in body.projects:
        new_project = Project(
            portfolio_id=portfolio.id,
            repo_name=project_data.repo_name,
            repo_url=project_data.repo_url,
            language=project_data.language,
            ai_description=project_data.ai_description,
            display_order=project_data.display_order
        )
        db.add(new_project)

    db.commit()

    return {"message": "Portfolio saved successfully", "portfolio_id": portfolio.id}


@router.get("/me", response_model=PortfolioResponse)
def get_my_portfolio(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get the logged-in user's saved portfolio (for editing).
    """
    portfolio = db.query(Portfolio).filter(Portfolio.user_id == current_user.id).first()

    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No portfolio found. Save one first."
        )

    return portfolio


@router.post("/publish")
def publish_portfolio(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mark the portfolio as published (publicly visible).
    """
    portfolio = db.query(Portfolio).filter(Portfolio.user_id == current_user.id).first()

    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No portfolio found. Save one first."
        )

    portfolio.is_published = True
    db.commit()

    return {
        "message": "Portfolio published!",
        "public_url": f"/p/{current_user.github_username}"
    }