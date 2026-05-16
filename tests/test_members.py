import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.database import Base
from app.api.routes.members import get_db

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

# ✅ Helper — Get Token
def get_token():
    client.post("/auth/register", json={
        "username": "memberuser",
        "password": "testpass123"
    })
    response = client.post("/auth/login", json={
        "username": "memberuser",
        "password": "testpass123"
    })
    return response.json()["access_token"]


def test_add_member():
    token = get_token()
    response = client.post("/members/", json={
        "name": "Ahmed Ali",
        "phone": "01012345678",
        "email": "ahmed@test.com"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["name"] == "Ahmed Ali"


def test_get_all_members():
    token = get_token()
    response = client.get("/members/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_search_member():
    token = get_token()
    response = client.get("/members/search?query=Ahmed",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200


def test_update_member():
    token = get_token()
    # Add member first
    add = client.post("/members/", json={
        "name": "Sara Mohamed",
        "phone": "01098765432"
    }, headers={"Authorization": f"Bearer {token}"})
    member_id = add.json()["id"]
    # Update
    response = client.put(f"/members/{member_id}", json={
        "name": "Sara Ahmed"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["name"] == "Sara Ahmed"


def test_delete_member():
    token = get_token()
    # Add member first
    add = client.post("/members/", json={
        "name": "To Delete",
        "phone": "01011111111"
    }, headers={"Authorization": f"Bearer {token}"})
    member_id = add.json()["id"]
    # Delete
    response = client.delete(f"/members/{member_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200


def test_get_member_not_found():
    token = get_token()
    response = client.get("/members/99999",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
