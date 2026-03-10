from fastapi import FastAPI
from app.routers import users, tasks

app = FastAPI(title="Productivity & Habit Analytics API")

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(users.router)
app.include_router(tasks.router)