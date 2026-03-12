from collections import defaultdict
from datetime import timedelta
from sqlalchemy.orm import Session

from app import models


def calculate_streaks_for_dates(dates):
    """
    dates: a list of Python date objects (already filtered to completed=True)
    returns: (current_streak, longest_streak)
    """
    if not dates:
        return 0, 0

    # Sort ascending for longest streak calculation
    sorted_dates = sorted(set(dates))

    # Longest streak
    longest_streak = 1
    current_run = 1

    for i in range(1, len(sorted_dates)):
        if sorted_dates[i] == sorted_dates[i - 1] + timedelta(days=1):
            current_run += 1
        else:
            longest_streak = max(longest_streak, current_run)
            current_run = 1

    longest_streak = max(longest_streak, current_run)

    # Current streak = count backwards from most recent date
    current_streak = 1
    latest = sorted_dates[-1]

    for i in range(len(sorted_dates) - 2, -1, -1):
        expected_prev = latest - timedelta(days=1)
        if sorted_dates[i] == expected_prev:
            current_streak += 1
            latest = sorted_dates[i]
        else:
            break

    return current_streak, longest_streak


def get_user_streaks(db: Session, user_id: int):
    habits = db.query(models.Habit).filter(models.Habit.user_id == user_id).all()

    results = []

    for habit in habits:
        logs = db.query(models.HabitLog).filter(
            models.HabitLog.habit_id == habit.id,
            models.HabitLog.completed == True
        ).all()

        log_dates = [log.date for log in logs]
        current_streak, longest_streak = calculate_streaks_for_dates(log_dates)

        results.append({
            "habit_id": habit.id,
            "habit_name": habit.name,
            "current_streak": current_streak,
            "longest_streak": longest_streak,
        })

    return results