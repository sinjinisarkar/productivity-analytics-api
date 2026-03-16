import holidays

from sqlalchemy.orm import Session
from app import models
from app.services.streaks import get_user_streaks
from datetime import date, timedelta, datetime
from collections import defaultdict


def get_productivity_score(db: Session, user_id: int):
    # ----- Tasks -----
    total_tasks = db.query(models.Task).filter(
        models.Task.user_id == user_id
    ).count()

    completed_tasks = db.query(models.Task).filter(
        models.Task.user_id == user_id,
        models.Task.completed == True
    ).count()

    task_score = 0
    if total_tasks > 0:
        task_score = (completed_tasks / total_tasks) * 50

    # ----- Habits / logs -----
    total_habits = db.query(models.Habit).filter(
        models.Habit.user_id == user_id
    ).count()

    completed_habit_logs = db.query(models.HabitLog).join(
        models.Habit
    ).filter(
        models.Habit.user_id == user_id,
        models.HabitLog.completed == True
    ).count()

    habit_score = min(completed_habit_logs * 5, 30) if total_habits > 0 else 0

    # ----- Streak bonus -----
    streak_data = get_user_streaks(db, user_id)

    longest_current_streak = 0
    if streak_data:
        longest_current_streak = max(item["current_streak"] for item in streak_data)

    streak_bonus = min(longest_current_streak * 2, 20)

    # ----- Final score -----
    productivity_score = round(task_score + habit_score + streak_bonus, 2)

    return {
        "productivity_score": productivity_score,
        "task_score": round(task_score, 2),
        "habit_score": round(habit_score, 2),
        "streak_bonus": round(streak_bonus, 2),
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "completed_habit_logs": completed_habit_logs,
        "best_current_streak": longest_current_streak,
    }

def get_weekly_progress(db: Session, user_id: int, start_date: date = None, end_date: date = None):
    today = date.today()

    # Use provided dates or default to current week
    if start_date:
        week_start = start_date
    else:
        week_start = today - timedelta(days=today.weekday())
    
    if end_date:
        week_end = end_date
    else:
        week_end = week_start + timedelta(days=6)

    # Tasks created this week
    tasks_created = db.query(models.Task).filter(
        models.Task.user_id == user_id,
        models.Task.created_at >= week_start
    ).count()

    # Tasks completed this week
    tasks_completed = db.query(models.Task).filter(
        models.Task.user_id == user_id,
        models.Task.completed == True,
        models.Task.completed_at != None,
        models.Task.completed_at >= week_start,
        models.Task.completed_at <= week_end
    ).count()

    # Habit logs completed this week
    habit_logs_completed = db.query(models.HabitLog).join(
        models.Habit
    ).filter(
        models.Habit.user_id == user_id,
        models.HabitLog.completed == True,
        models.HabitLog.date >= week_start,
        models.HabitLog.date <= week_end
    ).count()

    # UK public holidays during this period
    uk_holidays = holidays.UnitedKingdom(years=[week_start.year, week_end.year])

    holidays_in_week = []
    for holiday_date, holiday_name in uk_holidays.items():
        if week_start <= holiday_date <= week_end:
            holidays_in_week.append({
                "date": holiday_date.isoformat(),
                "name": holiday_name
            })

    return {
        "week_start": week_start,
        "week_end": week_end,
        "tasks_created": tasks_created,
        "tasks_completed": tasks_completed,
        "habit_logs_completed": habit_logs_completed,
        "holiday_count": len(holidays_in_week),
        "holidays": holidays_in_week,
    }

def get_heatmap_data(db: Session, user_id: int, days: int = 90):
    cutoff = date.today() - timedelta(days=days)
    activity = defaultdict(int)

    # Count completed tasks by completion date
    completed_tasks = db.query(models.Task).filter(
        models.Task.user_id == user_id,
        models.Task.completed == True,
        models.Task.completed_at != None,
        models.Task.completed_at >= cutoff
    ).all()

    for task in completed_tasks:
        day = task.completed_at.date().isoformat()
        activity[day] += 1

    # Count completed habit logs by date
    completed_logs = db.query(models.HabitLog).join(
        models.Habit
    ).filter(
        models.Habit.user_id == user_id,
        models.HabitLog.completed == True,
        models.HabitLog.date >= cutoff
    ).all()

    for log in completed_logs:
        day = log.date.isoformat()
        activity[day] += 1

    result = [
        {"date": day, "activity": count}
        for day, count in sorted(activity.items())
    ]

    return result