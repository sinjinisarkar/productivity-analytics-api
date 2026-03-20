from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, tasks, habits, auth, analytics

app = FastAPI(title="Productivity & Habit Analytics API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(habits.router)
app.include_router(auth.router)
app.include_router(analytics.router)