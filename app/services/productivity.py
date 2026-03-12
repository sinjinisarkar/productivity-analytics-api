from sqlalchemy.orm import Session
from app import models
from app.services.streaks import get_user_streaks
from datetime import date, timedelta



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

def get_weekly_progress(db: Session, user_id: int):
    today = date.today()

    # Monday start of the week
    week_start = today - timedelta(days=today.weekday())
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
        models.Task.completed_at >= week_start
    ).count()

    # Habit logs completed this week
    habit_logs_completed = db.query(models.HabitLog).join(
        models.Habit
    ).filter(
        models.Habit.user_id == user_id,
        models.HabitLog.completed == True,
        models.HabitLog.date >= week_start
    ).count()

    return {
        "week_start": week_start,
        "week_end": week_end,
        "tasks_created": tasks_created,
        "tasks_completed": tasks_completed,
        "habit_logs_completed": habit_logs_completed,
    }