# Productivity Analytics API
A backend REST API built with FastAPI that allows users to manage tasks and habits while generating behavioural productivity insights. The system provides analytics such as productivity scores, streak tracking, weekly progress metrics, activity heatmaps, and holiday-aware analytics.

## Project Overview
This project implements a productivity analytics backend that enables users to:
- Manage personal tasks
- Track daily habits
- Record habit completion logs
- Analyse productivity behaviour through analytics endpoints

The system is designed with a clean, modular architecture separating routers, services, models, and schemas. It uses JWT authentication to secure user-specific data and enforce strict ownership-based access control.

## Features
### Core features
- User registration and authentication
- JWT-based protected API endpoints
- Task management (create, update, complete tasks)
- Habit tracking
- Habit completion logging
- Duplicate log prevention
- User ownership protection

### Analytics Features
- Productivity score calculation
- Habit streak tracking
- Weekly productivity analytics
- Activity heatmap generation
- Holiday-aware weekly analytics using UK public holiday integration

## Tech Stack
- FastAPI – API framework
- SQLAlchemy – ORM for database operations
- SQLite – database for development and testing
- Alembic – database migrations
- JWT Authentication – secure user authentication
- Pytest – automated testing
- Python Holidays Library – UK public holiday integration
- Swagger UI / OpenAPI – interactive API documentation

## Project Structure
```
productivity-analytics-api/
├── alembic/                    # Database migration files
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── app/
│   ├── core/
│   │   ├── config.py           # App settings and environment variables
│   │   └── security.py         # Password hashing and JWT utilities
│   ├── routers/
│   │   ├── analytics.py        # Analytics endpoints (streaks, summaries, heatmaps)
│   │   ├── auth.py             # Authentication (login, JWT token issuing)
│   │   ├── habits.py           # Habits and habit logs CRUD
│   │   ├── tasks.py            # Tasks CRUD
│   │   └── users.py            # Users CRUD
│   ├── services/
│   │   ├── productivity.py     # Productivity summary logic
│   │   ├── streaks.py          # Habit streak calculation logic
│   │   └── summaries.py        # Aggregation and reporting logic
│   ├── tests/
│   │   ├── conftest.py         # Test database setup and fixtures
│   │   ├── test_habits.py      # Habit endpoint tests
│   │   ├── test_tasks.py       # Task endpoint tests
│   │   └── test_users.py       # User endpoint tests
│   ├── __init__.py
│   ├── database.py             # SQLAlchemy engine and session setup
│   ├── dependencies.py         # get_current_user JWT dependency
│   ├── main.py                 # FastAPI app entry point
│   ├── models.py               # SQLAlchemy ORM models
│   └── schemas.py              # Pydantic request/response schemas
├──frontend/
│   ├── app.js  
│   ├── index.html         
│   └── styles.css         
├── .gitignore
├── alembic.ini                 # Alembic configuration
├── README.md
└── requirements.txt
```

## Installation and Setup
### 1. Clone the repository
```bash
git clone <your-repo-link>
cd productivity-analytics-api
```

### 2. Create virtual environment
```bash
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run database migrations
```bash
alembic upgrade head
```

### 5. Run the server
```bash
uvicorn app.main:app --reload
```

## Live deployment
**Backend API:**  
https://productivity-analytics-api.onrender.com/docs

**Frontend Dashboard:**  
https://productivity-analytics-api-1.onrender.com/


## API Documentation
The full API documentation is available as a PDF: [API Documentation](./docs/api-documentation.pdf)

Or view it live at: https://productivity-analytics-api.onrender.com/redoc

This provides:
- Interactive endpoint testing
- Request/response schemas
- JWT authentication via the Authorize button

## Analytics Overview
The system goes beyond CRUD by providing:
- Behavioural insights (streaks)
- Performance scoring (productivity score)
- Time-based trends (weekly analytics)
- Visual activity patterns (heatmap)
- Context-aware analysis (public holidays)

## Design Decisions
- FastAPI chosen for high-performance API development and automatic documentation
- Service layer architecture used to separate business logic from routes
- JWT authentication ensures secure user-specific data access
- Modular structure improves scalability and maintainability

## Testing
Run tests using: 
```bash
python -m pytest -q
```
Includes:
- Authentication tests
- Task and habit endpoint tests
- Analytics validation