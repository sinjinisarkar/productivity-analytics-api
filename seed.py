import csv
import sys
import os
from datetime import date, timedelta
import random

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine
from app import models
from app.core.security import hash_password

# Create all tables
models.Base.metadata.create_all(bind=engine)

def seed():
    db = SessionLocal()

    try:
        # Check if already seeded
        if db.query(models.User).count() > 0:
            print("Database already seeded, skipping.")
            return

        print("Seeding database from student habits dataset...")

        dataset_path = os.path.join(os.path.dirname(__file__), "enhanced_student_habits_performance_dataset.csv")

        with open(dataset_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)[:50]  # Only use first 50 students

        today = date.today()

        for i, row in enumerate(rows):
            # ── Create user ──────────────────────────────────────
            username = f"student_{row['student_id']}"
            email = f"student{row['student_id']}@example.com"

            user = models.User(
                username=username,
                email=email,
                hashed_password=hash_password("Password123"),
            )
            db.add(user)
            db.flush()  # Get user.id

            # ── Create habits from dataset columns ───────────────
            habit_map = [
                ("Daily Study", "daily", float(row["study_hours_per_day"]) >= 3),
                ("Exercise", "daily", int(row["exercise_frequency"]) >= 3),
                ("Sleep 8 Hours", "daily", float(row["sleep_hours"]) >= 7),
                ("Limit Social Media", "daily", float(row["social_media_hours"]) <= 2),
            ]

            for habit_name, frequency, is_consistent in habit_map:
                habit = models.Habit(
                    user_id=user.id,
                    name=habit_name,
                    frequency=frequency,
                )
                db.add(habit)
                db.flush()

                # Generate habit logs for last 30 days
                for day_offset in range(30):
                    log_date = today - timedelta(days=day_offset)
                    # Consistent students log more frequently
                    if is_consistent:
                        completed = random.random() < 0.8
                    else:
                        completed = random.random() < 0.4

                    if completed:
                        log = models.HabitLog(
                            habit_id=habit.id,
                            date=log_date,
                            completed=True,
                        )
                        db.add(log)

            # ── Create tasks from dataset ────────────────────────
            attendance = float(row["attendance_percentage"])
            motivation = int(row["motivation_level"])
            study_hours = float(row["study_hours_per_day"])

            task_templates = [
                f"Complete {row['major']} assignment",
                f"Study for {study_hours:.1f} hours",
                "Attend lecture",
                "Review lecture notes",
                "Submit weekly report",
                "Prepare for exam",
                "Group study session",
                "Online quiz",
            ]

            for j, title in enumerate(task_templates):
                # High attendance/motivation = more completed tasks
                completed = random.random() < (attendance / 100)
                due_date = today - timedelta(days=random.randint(0, 30))

                task = models.Task(
                    user_id=user.id,
                    title=title,
                    description=f"Generated from student dataset - Motivation: {motivation}/10",
                    due_date=due_date,
                    completed=completed,
                    completed_at=due_date if completed else None,
                )
                db.add(task)

        db.commit()
        print(f"Successfully seeded {len(rows)} users with habits, logs, and tasks!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()