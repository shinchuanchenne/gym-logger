# GymLogger

## Overview

GymLogger is a backend API project for tracking workouts and exercise logs.
It allows users to register, log in with JWT authentication, create and manage workouts, and add exercise logs under each workout.

This project was built with FastAPI, SQLModel, PostgreSQL, Alembic, and Pytest.  
It also includes ownership-based access control, so users can only access and modify their own workout data.

## Tech Stack

- **FastAPI** - backend API framework
- **SQLModel** - ORM and data modelling
- **PostgreSQL** - primary relational database
- **Alembic** - database migrations
- **JWT Authentication** - token-based authentication
- **Pytest** - automated testing
- **Pydantic / pydantic-settings** - data validation and configuration management
- **pwdlib (Argon2)** - password hashing

## Features

- User registration
- JWT-based login authentication
- Retrieve current authenticated user
- Create, read, update, and delete workouts
- Ownership-based workout access control
- Create exercise logs under workouts
- Ownership-based exercise log access control
- Nested workout detail response with exercise logs
- Automated API tests with a dedicated PostgreSQL test database

## Project Structure

```text
gym_logger/
├── app/
│   ├── core/           # configuration, security, authentication helpers
│   ├── db/             # database engine and session management
│   ├── models/         # SQLModel models
│   ├── repositories/   # database access layer
│   ├── routers/        # API endpoints
│   ├── schemas/        # request/response schemas
│   ├── services/       # business logic layer
│   └── main.py         # FastAPI application entry point
├── tests/              # pytest test suite
├── alembic/            # database migration files
├── .env                # environment variables
├── alembic.ini         # Alembic configuration
├── requirements.txt    # Python dependencies
└── README.md           # project documentation
```
