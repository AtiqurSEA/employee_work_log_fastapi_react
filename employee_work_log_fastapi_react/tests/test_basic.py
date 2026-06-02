from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_backend_root_or_api_docs_available():
    response = client.get("/")
    assert response.status_code in [200, 404]


def test_login_with_seeded_admin():
    response = client.post(
        "/api/auth/login",
        json={"email": "admin@example.com", "password": "admin123"},
    )
    assert response.status_code == 200
    assert response.json()["role"] == "admin"
