import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine


from app.main import app
from app.db.session import get_session
from app.core.config import settings
from app.models import User, Workout, ExerciseLog

test_engine = create_engine(settings.TEST_DATABASE_URL)

@pytest.fixture
def db_session():
    SQLModel.metadata.drop_all(test_engine)
    SQLModel.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        yield session


@pytest.fixture
def client(db_session):
    def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()