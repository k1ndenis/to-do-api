import pytest
from fastapi.testclient import TestClient

class TestListsAPI:
    def test_create_list(self, client: TestClient):
        response = client.post("/api/lists", json={"title": "Test List"})
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test List"
        assert "id" in data
        assert data["tasks"] == []

    def test_get_all_lists(self, client: TestClient):
        client.post("/api/lists", json={"title": "List 1"})
        client.post("/api/lists", json={"title": "List 2"})

        response = client.get("/api/lists")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_delete_list(self, client: TestClient):
        create_resp = client.post("/api/lists", json={"title": "Test List"})
        list_id = create_resp.json()["id"]

        delete_resp = client.delete(f"/api/lists/{list_id}")
        assert delete_resp.status_code == 204

        get_resp = client.get("api/lists")
        assert len(get_resp.json()) == 0
    
    def test_delete_nonexistent_list(self, client: TestClient):
        response = client.delete("/api/lists/non-existent-id")
        assert response.status_code == 404

        