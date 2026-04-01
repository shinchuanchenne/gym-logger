# GymLogger

A personal workout logging backend project built with FastAPI.

## Overview

GymLogger is a backend API project for tracking workouts and exercise logs.

It allows users to:

- register and log in with JWT authentication
- create, view, update, and delete workouts
- add exercise logs under a workout
- access only their own workout data through ownership-based access control

The project is built with FastAPI, SQLModel, PostgreSQL, Alembic, and Pytest.
It also includes a minimal frontend demo and Docker-based local development setup.

## Tech Stack

- **Python**
- **FastAPI** - backend API framework
- **SQLModel** - ORM and data modelling
- **PostgreSQL** - relational database
- **Alembic** - database migrations
- **JWT Authentication** - token-based authentication
- **Pydantic / pydantic-settings** - validation and configuration management
- **pwdlib (Argon2)** - password hashing
- **Pytest** - automated API testing
- **Docker / Docker Compose** - containerised local development
- **HTML / CSS / JavaScript** - minimal frontend demo

## Features

- User registration
- JWT-based login authentication
- Retrieve current authenticated user
- Create, read, update, and delete workouts
- Ownership-based workout access control
- Create, read, update, and delete exercise logs under workouts
- Ownership-based exercise log access control
- Nested workout detail response with exercise logs
- PostgreSQL database integration
- Alembic migration support
- Automated API tests with a dedicated PostgreSQL test database
- Minimal frontend pages for login, registration, workout list, and workout detail

## Project Structure

```text
gym_logger/
├── app/
│   ├── core/              # configuration, security, authentication helpers
│   ├── db/                # database engine and session management
│   ├── models/            # SQLModel models
│   ├── repositories/      # database access layer
│   ├── routers/           # API endpoints
│   ├── schemas/           # request/response schemas
│   ├── services/          # business logic layer
│   └── main.py            # FastAPI application entry point
├── frontend/
│   ├── css/               # frontend styles
│   ├── js/                # frontend API and page logic
│   ├── login.html
│   ├── register.html
│   ├── workouts.html
│   └── workout-detail.html
├── tests/                 # pytest test suite
├── alembic/               # Alembic migration files
├── Dockerfile             # backend container image
├── docker-compose.yml     # local multi-container setup
├── alembic.ini            # Alembic configuration
├── requirements.txt       # Python dependencies
├── requirements-lock.txt  # locked dependency versions
├── test_db_connection.py  # simple database connection check
└── README.md              # project documentation
```

## API Overview

### Authentication

- `POST /auth/register` - register a new user

- `POST /auth/token` - log in and receive JWT token

- `GET /users/me` - retrieve current authenticated user

### Workouts

- `POST /workouts` - create a workout

- `GET /workouts` - list workouts

- `GET /workouts/{id}` - retrieve workout detail

- `PUT /workouts/{id}` - update a workout

- `DELETE /workouts/{id}` - delete a workout

### Exercise Logs

- `POST /workouts/{workout_id}/exercise-logs` - create an exercise log
- `GET /workouts/{workout_id}/exercise-logs` - list exercise logs for a workout
- `GET /workouts/{workout_id}/exercise-logs/{exercise_log_id}` - retrieve a single exercise log
- `PUT /workouts/{workout_id}/exercise-logs/{exercise_log_id}` - update an exercise log
- `DELETE /workouts/{workout_id}/exercise-logs/{exercise_log_id}` - delete an exercise log

## Setup

### Prerequisites

- Python 3.13+
- PostgreSQL
- Git
- Docker

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd gym_logger
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

Create a `.env` file in the project root and add the required environment variables.

Example:

```bash
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/gym_logger
TEST_DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/gym_logger_test
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256
```

Update the database username, password, host, port, and database name according to your local PostgreSQL setup.

### 5.Create the databases

Make sure both development and test databases exist in PostgreSQL.

Example:

```bash
CREATE DATABASE gym_logger;
CREATE DATABASE gym_logger_test;
```

### 6. Run database migrations

```bash
alembic upgrade head
```

This will create the required tables in the development database.

### 7. Start the backend server

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```bash
http://127.0.0.1:8000
```

Swagger UI:

```bash
http://127.0.0.1:8000/docs
```

### 8. Run the tests

```bash
pytest
```

This will run the automated test suite against the test database.

### Optional: Run with Docker

If you want to run the project with Docker instead of a local Python environment:

```bash
docker compose up --build
```

To stop the containers:

```bash
docker compose down
```

## Demo Flow

A minimal frontend demo is included to show the core user flow of the project.

### 1. Register

Create a new user account from the registration page.

### 2. Log in

Log in with the registered account and receive a JWT access token.

### 3. View workout list

After login, the user can view their own workout records.

### 4. Create a workout

The user can create a new workout by entering the workout title, date, and optional notes.

### 5. Open workout detail

The user can open a workout detail page to view the selected workout and its exercise logs.

### 6. Add exercise logs

Inside the workout detail page, the user can add exercise logs under that workout.

### 7. Update or delete records

The user can update or delete workouts and exercise logs, with ownership rules applied so only the owner can modify their own data.

### 8. Backend verification

All frontend actions are sent to the FastAPI backend, which validates JWT authentication, checks ownership, and persists data in PostgreSQL.
