from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.routes.portal import get_db
from app.db.database import Base
from app.main import app

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
        "username": "portaladmin",
        "password": "testpass123"
    })
    response = client.post("/auth/login", json={
        "username": "portaladmin",
        "password": "testpass123"
    })
    return response.json()["access_token"]


def test_member_can_join_from_portal_and_appear_in_dashboard():
    join = client.post("/portal/join", json={
        "name": "Portal Member",
        "phone": "01033333333",
        "email": "portal@example.com",
        "plan": "monthly"
    })

    assert join.status_code == 200
    assert join.json()["member_id"] == 1
    assert join.json()["status"] == "active"

    token = get_token()
    stats = client.get(
        "/dashboard/stats",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert stats.status_code == 200
    assert stats.json()["total_members"] == 1
    assert stats.json()["active_subscriptions"] == 1
    assert stats.json()["monthly_plans"] == 1


def test_portal_rejects_duplicate_member_contact():
    client.post("/portal/join", json={
        "name": "First Member",
        "phone": "01044444444",
        "email": "duplicate@example.com",
        "plan": "yearly"
    })

    duplicate = client.post("/portal/join", json={
        "name": "Second Member",
        "phone": "01044444444",
        "email": "other@example.com",
        "plan": "monthly"
    })

    assert duplicate.status_code == 400
