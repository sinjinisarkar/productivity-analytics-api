from sqlalchemy.orm import Session
from app import models


def get_user_summary(db: Session, user_id: int):
    # Total tasks
    total_tasks = db.query(models.Task).filter(
        models.Task.user_id == user_id
    ).count()

    # Completed tasks
    completed_tasks = db.query(models.Task).filter(
        models.Task.user_id == user_id,
        models.Task.completed == True
    ).count()

    # Total habits
    total_habits = db.query(models.Habit).filter(
        models.Habit.user_id == user_id
    ).count()

    # Total habit logs
    total_habit_logs = db.query(models.HabitLog).join(
        models.Habit
    ).filter(
        models.Habit.user_id == user_id
    ).count()

    completion_rate = 0
    if total_tasks > 0:
        completion_rate = completed_tasks / total_tasks

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "completion_rate": completion_rate,
        "total_habits": total_habits,
        "total_habit_logs": total_habit_logs,
    }