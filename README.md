# Productivity Analytics API
A backend REST API built with FastAPI that allows users to manage tasks and habits while generating behavioural productivity insights. The system provides analytics such as productivity scores, streak tracking, weekly progress metrics, activity heatmaps, and holiday-aware analytics.

## Project Overview
This project implements a productivity analytics backend that enables users to:
- Manage personal tasks
- Track daily habits
- Record habit completion logs
- Analyse productivity behaviour through analytics endpoints

The system is designed with a clean architecture separating routers, services, models, and schemas. It uses JWT authentication to secure user-specific data and ensure proper ownership isolation.

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
├── .gitignore
├── alembic.ini                 # Alembic configuration
├── README.md
└── requirements.txt
```