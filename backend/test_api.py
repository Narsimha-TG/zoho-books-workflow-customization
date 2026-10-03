import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_generate_quote_success():
    payload = {
        "quote_id": "Q-2002",
        "template_type": "Project",
        "client_id": "C-99"
    }
    response = client.post("/api/v1/quote/generate", json=payload)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["quote_id"] == "Q-2002"
    assert data["status"] == "Generated"
    assert "pdf_url" in data

def test_webhook_update_success():
    # First ensure quote exists
    client.post("/api/v1/quote/generate", json={"quote_id": "Q-3003", "template_type": "Generic", "client_id": "C-01"})
    
    payload = {"quote_id": "Q-3003", "status": "Approved"}
    response = client.post("/api/v1/webhook/zoho-books", json=payload)
    assert response.status_code == 200
    assert response.json() == {"status": "success"}

def test_get_metadata():
    response = client.get("/api/v1/templates/metadata")
    assert response.status_code == 200
    data = response.json()
    assert "templates" in data
    assert "mapping" in data
    assert data["mapping"]["Project"] == "P-001"

def test_webhook_not_found():
    payload = {"quote_id": "NON-EXISTENT", "status": "Approved"}
    response = client.post("/api/v1/webhook/zoho-books", json=payload)
    assert response.status_code == 404