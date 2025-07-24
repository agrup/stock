from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)


def test_create_user_conflict(override_sql_use_case):
    # Primer usuario creado exitosamente
    payload = {"name": "Agustin ro", "email": "agus@example.com"}
    res1 = client.post("/v1/users", json=payload)
    assert res1.status_code == 200

    # Segundo intento con el mismo email → debería fallar
    res2 = client.post("/v1/users", json=payload)
    assert res2.status_code == 409
    assert res2.json() == {"detail": "El usuario ya existe"}


def test_create_user_with_invalid_name(override_sql_use_case):
    payload = {"name": "Agustin", "email": "agus@example.com"}
    response = client.post("/v1/users", json=payload)
    assert response.status_code == 422
    assert response.json() == {"detail": "El nombre debe tener al menos dos palabras"}
