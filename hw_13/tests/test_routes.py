import pytest
from fastapi.testclient import TestClient

from my_contacts_api.main import app, models, crud, database
from my_contacts_api.app.database import SessionLocal

client = TestClient(app)

@pytest.fixture(scope="module")
def test_db():
    database.Base.metadata.create_all(bind=database.engine)
    db = SessionLocal()
    yield db
    db.close()
    database.Base.metadata.drop_all(bind=database.engine)

def test_create_user(test_db):
    response = client.post("/users/", json={"email": "test@example.com", "password": "password"})
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"

def test_login(test_db):
    response = client.post("/token", data={"username": "test@example.com", "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_create_contact(test_db):
    token_response = client.post("/token", data={"username": "test@example.com", "password": "password"})
    access_token = token_response.json()["access_token"]
    response = client.post("/contacts/", json={"name": "Test Contact", "email": "contact@example.com", "phone": "123456789"}, headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 201
    assert response.json()["name"] == "Test Contact"
