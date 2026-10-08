from fastapi.testclient import TestClient
from app.main import app
from app.services.db_service import init_db

# Ensure DB is seeded
init_db()
client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["health"] == "OK"

def test_get_zones():
    response = client.get("/api/zones")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 8
    assert data[0]["id"] == "Z1"

def test_get_roads():
    response = client.get("/api/roads")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 17
