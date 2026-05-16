import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.database import Base
from app.api.routes.auth import get_db

# ✅ SQLite للـ Testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
Base.metadata.create_all(bind=engine)
client = TestClient(app)


def test_register_success():
    response = client.post("/auth/register", json={
        "username": "testuser",
        "password": "testpass123"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "User created successfully"


def test_register_duplicate():
    client.post("/auth/register", json={
        "username": "dupuser",
        "password": "testpass123"
    })
    response = client.post("/auth/register", json={
        "username": "dupuser",
        "password": "testpass123"
    })
    assert response.status_code == 400


def test_login_success():
    client.post("/auth/register", json={
        "username": "loginuser",
        "password": "testpass123"
    })
    response = client.post("/auth/login", json={
        "username": "loginuser",
        "password": "testpass123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password():
    response = client.post("/auth/login", json={
        "username": "loginuser",
        "password": "wrongpass"
    })
    assert response.status_code == 401


def test_login_wrong_username():
    response = client.post("/auth/login", json={
        "username": "nobody",
        "password": "testpass123"
    })
    assert response.status_code == 401
