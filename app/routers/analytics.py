from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.dependencies import get_current_user
from app import models
from app.services.summaries import get_user_summary
from app.services.streaks import get_user_streaks
from app.services.productivity import get_productivity_score
from app.services.productivity import get_weekly_progress
from app.services.productivity import get_heatmap_data
from fastapi import APIRouter, Depends, Query
from app.schemas import SummaryOut, StreakItem, ProductivityOut, WeeklyOut, HeatmapItem
from typing import List, Optional

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/summary", response_model=SummaryOut)
def analytics_summary(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return get_user_summary(db, current_user.id)


@router.get("/streaks", response_model=List[StreakItem])
def analytics_streaks(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return get_user_streaks(db, current_user.id)


@router.get("/productivity", response_model=ProductivityOut)
def analytics_productivity(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return get_productivity_score(db, current_user.id)


@router.get("/weekly", response_model=WeeklyOut)
def analytics_weekly(
    start_date: Optional[date] = Query(default=None, description="Start date (defaults to Monday of current week)"),
    end_date: Optional[date] = Query(default=None, description="End date (defaults to Sunday of current week)"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return get_weekly_progress(db, current_user.id, start_date=start_date, end_date=end_date)


@router.get("/heatmap", response_model=List[HeatmapItem])
def analytics_heatmap(
    days: int = Query(default=90, le=365, description="Number of past days to include (max 365)"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return get_heatmap_data(db, current_user.id, days=days)