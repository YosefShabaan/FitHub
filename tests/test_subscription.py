import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date

from app.main import app
from app.db.database import Base
from app.api.routes.subscriptions import get_db

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

def get_token():
    client.post("/auth/register", json={
        "username": "subuser",
        "password": "testpass123"
    })
    res = client.post("/auth/login", json={
        "username": "subuser",
        "password": "testpass123"
    })
    return res.json()["access_token"]

def create_test_member(token):
    res = client.post("/members/", json={
        "name": "Sub Member",
        "phone": "01022222222"
    }, headers={"Authorization": f"Bearer {token}"})
    return res.json()["id"]


def test_create_subscription():
    token = get_token()
    member_id = create_test_member(token)
    response = client.post("/subscriptions/", json={
        "member_id": member_id,
        "plan": "monthly",
        "start_date": str(date.today())
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["status"] == "active"


def test_subscription_end_date_monthly():
    token = get_token()
    member_id = create_test_member(token)
    response = client.post("/subscriptions/", json={
        "member_id": member_id,
        "plan": "monthly",
        "start_date": "2024-01-01"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.json()["end_date"] == "2024-01-31"


def test_subscription_end_date_yearly():
    token = get_token()
    member_id = create_test_member(token)
    response = client.post("/subscriptions/", json={
        "member_id": member_id,
        "plan": "yearly",
        "start_date": "2024-01-01"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.json()["end_date"] == "2024-12-31"


def test_get_all_subscriptions():
    token = get_token()
    response = client.get("/subscriptions/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200


def test_dashboard_stats():
    token = get_token()
    response = client.get("/dashboard/stats",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "total_members" in data
    assert "active_subscriptions" in data
    assert "expired_subscriptions" in data
