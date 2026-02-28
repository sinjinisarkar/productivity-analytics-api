from fastapi import FastAPI

app = FastAPI(title="Productivity & Habit Analytics API")

@app.get("/health")
def health():
    return {"status": "ok"}