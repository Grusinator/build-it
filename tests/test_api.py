import pytest
from fastapi.testclient import TestClient
from main import app  # adjust the import based on your FastAPI application structure

client = TestClient(app)


def test_get_collection_endpoint():
    response = client.get("/collection")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"

    # Validate the structure of the response
    json_response = response.json()
    assert isinstance(json_response, list)
    for box in json_response:
        assert "start" in box
        assert "end" in box
        assert "x" in box["start"]
        assert "y" in box["start"]
        assert "z" in box["start"]
        assert "x" in box["end"]
        assert "y" in box["end"]
        assert "z" in box["end"]
