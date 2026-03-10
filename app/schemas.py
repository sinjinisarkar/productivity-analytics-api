from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime, date
from typing import Optional

# User schemas
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(default=None, min_length=3, max_length=30)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(default=None, min_length=8, max_length=72)


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Task schemas 
class TaskCreate(BaseModel):
    user_id: int
    title: str = Field(min_length=1, max_length=120)
    description: Optional[str] = Field(default=None, max_length=500)
    due_date: Optional[date] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=120)
    description: Optional[str] = Field(default=None, max_length=500)
    due_date: Optional[date] = None
    completed: Optional[bool] = None  # if set True, we auto-set completed_at

class TaskOut(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str]
    due_date: Optional[date]
    completed: bool
    completed_at: Optional[datetime]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Habit schemas
class HabitCreate(BaseModel):
    user_id: int
    name: str = Field(min_length=1, max_length=100)
    frequency: str = Field(default="daily", pattern="^(daily|weekly)$")

class HabitUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    frequency: Optional[str] = Field(default=None, pattern="^(daily|weekly)$")

class HabitOut(BaseModel):
    id: int
    user_id: int
    name: str
    frequency: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class HabitLogCreate(BaseModel):
    date: date
    completed: bool = True

class HabitLogOut(BaseModel):
    id: int
    habit_id: int
    date: date
    completed: bool

    model_config = ConfigDict(from_attributes=True)