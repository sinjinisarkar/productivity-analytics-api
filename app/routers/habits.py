from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.database import get_db
from app import models
from app.schemas import HabitCreate, HabitUpdate, HabitOut, HabitLogCreate, HabitLogOut

router = APIRouter(prefix="/habits", tags=["Habits"])


# ── Habit CRUD ─────────────────────────────────────────────

@router.post("", response_model=HabitOut, status_code=status.HTTP_201_CREATED)
def create_habit(payload: HabitCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    habit = models.Habit(
        user_id=payload.user_id,
        name=payload.name,
        frequency=payload.frequency,
    )
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return habit


@router.get("", response_model=List[HabitOut])
def list_habits(
    db: Session = Depends(get_db),
    user_id: Optional[int] = None,
    limit: int = Query(default=20, le=100),
    offset: int = 0,
):
    q = db.query(models.Habit)
    if user_id is not None:
        q = q.filter(models.Habit.user_id == user_id)
    return q.order_by(models.Habit.created_at.desc()).limit(limit).offset(offset).all()


@router.get("/{habit_id}", response_model=HabitOut)
def get_habit(habit_id: int, db: Session = Depends(get_db)):
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found.")
    return habit


@router.patch("/{habit_id}", response_model=HabitOut)
def update_habit(habit_id: int, payload: HabitUpdate, db: Session = Depends(get_db)):
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found.")

    if payload.name is not None:
        habit.name = payload.name
    if payload.frequency is not None:
        habit.frequency = payload.frequency

    db.commit()
    db.refresh(habit)
    return habit


@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit(habit_id: int, db: Session = Depends(get_db)):
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found.")
    db.delete(habit)
    db.commit()
    return None


# ── Habit Log CRUD ─────────────────────────────────────────

@router.post("/{habit_id}/logs", response_model=HabitLogOut, status_code=status.HTTP_201_CREATED)
def log_habit(habit_id: int, payload: HabitLogCreate, db: Session = Depends(get_db)):
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found.")

    # Prevent duplicate logs for the same date
    existing = db.query(models.HabitLog).filter(
        models.HabitLog.habit_id == habit_id,
        models.HabitLog.date == payload.date,
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Log already exists for this date.")

    log = models.HabitLog(
        habit_id=habit_id,
        date=payload.date,
        completed=payload.completed,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


@router.get("/{habit_id}/logs", response_model=List[HabitLogOut])
def list_habit_logs(
    habit_id: int,
    db: Session = Depends(get_db),
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    limit: int = Query(default=30, le=365),
    offset: int = 0,
):
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found.")

    q = db.query(models.HabitLog).filter(models.HabitLog.habit_id == habit_id)
    if from_date:
        q = q.filter(models.HabitLog.date >= from_date)
    if to_date:
        q = q.filter(models.HabitLog.date <= to_date)

    return q.order_by(models.HabitLog.date.desc()).limit(limit).offset(offset).all()


@router.delete("/{habit_id}/logs/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit_log(habit_id: int, log_id: int, db: Session = Depends(get_db)):
    log = db.query(models.HabitLog).filter(
        models.HabitLog.id == log_id,
        models.HabitLog.habit_id == habit_id,
    ).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found.")
    db.delete(log)
    db.commit()
    return None