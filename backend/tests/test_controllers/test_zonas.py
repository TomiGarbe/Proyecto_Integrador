import pytest
from fastapi.testclient import TestClient
from src.api.routes import app
from src.config.database import SessionLocal

client = TestClient(app)

def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides = {}
created_zona_id = None

def test_create_zona():
    global created_zona_id
    response = client.post("/zonas/", json={
        "nombre": "Zona Test"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Zona Test"
    assert "id" in data
    created_zona_id = data["id"]

def test_create_zona_already_exists():
    response = client.post("/zonas/", json={
        "nombre": "Zona Test"
    })
    assert response.status_code == 400
    assert "ya existe" in response.json()["detail"]

def test_listar_zonas():
    response = client.get("/zonas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_zona():
    global created_zona_id
    delete_response = client.delete(f"/zonas/{created_zona_id}")
    assert delete_response.status_code == 200
    assert "eliminada" in delete_response.json()["message"]

def test_delete_zona_not_found():
    response = client.delete("/zonas/9999999")
    assert response.status_code == 404
    assert "no encontrada" in response.json()["detail"]