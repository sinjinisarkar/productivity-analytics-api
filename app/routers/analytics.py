from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app import models
from app.services.summaries import get_user_summary
from app.services.streaks import get_user_streaks
from app.services.productivity import get_productivity_score
from app.services.productivity import get_weekly_progress
from app.services.productivity import get_heatmap_data



router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/summary")
def analytics_summary(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return get_user_summary(db, current_user.id)


@router.get("/streaks")
def analytics_streaks(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return get_user_streaks(db, current_user.id)


@router.get("/productivity")
def analytics_productivity(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return get_productivity_score(db, current_user.id)


@router.get("/weekly")
def analytics_weekly(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return get_weekly_progress(db, current_user.id)


@router.get("/heatmap")
def analytics_heatmap(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return get_heatmap_data(db, current_user.id)