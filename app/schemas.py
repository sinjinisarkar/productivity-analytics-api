from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime, date as date_type
from typing import Optional

# User schemas
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=30, examples=["student_1001"])
    email: EmailStr = Field(examples=["student1001@example.com"])
    password: str = Field(min_length=8, max_length=72, examples=["Password123"])


class UserUpdate(BaseModel):
    username: Optional[str] = Field(default=None, min_length=3, max_length=30, examples=["student_1001"])
    email: Optional[EmailStr] = Field(default=None, examples=["student1001@example.com"])
    password: Optional[str] = Field(default=None, min_length=8, max_length=72, examples=["NewPassword123"])


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Task schemas
class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120, examples=["Complete Computer Science assignment"])
    description: Optional[str] = Field(default=None, max_length=500, examples=["Generated from student dataset - Motivation: 8/10"])
    due_date: Optional[date_type] = Field(default=None, examples=["2026-03-27"])

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=120, examples=["Review lecture notes"])
    description: Optional[str] = Field(default=None, max_length=500, examples=["Focus on chapters 4 and 5"])
    due_date: Optional[date_type] = Field(default=None, examples=["2026-03-27"])
    completed: Optional[bool] = Field(default=None, examples=[True])

class TaskOut(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str]
    due_date: Optional[date_type]
    completed: bool
    completed_at: Optional[datetime]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Habit schemas
class HabitCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100, examples=["Daily Study"])
    frequency: str = Field(default="daily", pattern="^(daily|weekly)$", examples=["daily"])

class HabitUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100, examples=["Sleep 8 Hours"])
    frequency: Optional[str] = Field(default=None, pattern="^(daily|weekly)$", examples=["daily"])

class HabitOut(BaseModel):
    id: int
    user_id: int
    name: str
    frequency: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class HabitLogCreate(BaseModel):
    date: date_type = Field(examples=["2026-03-20"])
    completed: bool = Field(default=True, examples=[True])

class HabitLogOut(BaseModel):
    id: int
    habit_id: int
    date: date_type
    completed: bool

    model_config = ConfigDict(from_attributes=True)

# ── Analytics schemas ──────────────────────────────────────

class SummaryOut(BaseModel):
    total_tasks: int
    completed_tasks: int
    completion_rate: float
    total_habits: int
    total_habit_logs: int

class StreakItem(BaseModel):
    habit_id: int
    habit_name: str
    current_streak: int
    longest_streak: int

class ProductivityOut(BaseModel):
    productivity_score: float
    task_score: float
    habit_score: float
    streak_bonus: float
    total_tasks: int
    completed_tasks: int
    completed_habit_logs: int
    best_current_streak: int

class WeeklyOut(BaseModel):
    week_start: date_type
    week_end: date_type
    tasks_created: int
    tasks_completed: int
    habit_logs_completed: int
    holiday_count: int
    holidays: list

class HeatmapItem(BaseModel):
    date: str
    activity: int
