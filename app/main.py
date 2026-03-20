from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, tasks, habits, auth, analytics

app = FastAPI(
    title="Productivity & Habit Analytics API",
    version="0.1.0",
    description="""
A RESTful API for tracking productivity tasks, habits, and personal analytics.

## Features
- **Users** — Register and manage user accounts
- **Tasks** — Create and track to-do items with due dates
- **Habits** — Log daily/weekly habits and track streaks  
- **Analytics** — Productivity scores, heatmaps, and weekly summaries

## Authentication
Most endpoints require a Bearer token. Use `POST /auth/login` to obtain one.
"""
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://productivity-analytics-api-1.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok"}

app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(habits.router)
app.include_router(auth.router)
app.include_router(analytics.router)