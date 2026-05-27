import pytest
from fastapi.testclient import TestClient

class TestTasksAPI:
    @pytest.fixture
    def list_id(self, client: TestClient):
        response = client.post("/api/lists", json={"title": "Test List"})
        return response.json()["id"]
    
    def test_create_task(self, client: TestClient, list_id: str):
        response = client.post(
            f"/api/lists/{list_id}/tasks",
            json={"title": "Test Task"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Task"
        assert data["completed"] is False
        assert data["listId"] == list_id

    def test_toggle_task_completion(self, client: TestClient, list_id: str):
        create_resp = client.post(
            f"/api/lists/{list_id}/tasks",
            json={"title": "Test Task"}
        )
        task_id = create_resp.json()["id"]

        toggle_resp = client.patch(
            f"/api/lists/{list_id}/tasks/{task_id}/toggle"
        )
        assert toggle_resp.status_code == 200
        assert toggle_resp.json()["completed"] is True

        toggle_resp_2 = client.patch(
            f"/api/lists/{list_id}/tasks/{task_id}/toggle"
        )
        assert toggle_resp_2.status_code == 200
        assert toggle_resp_2.json()["completed"] is False
    
    def test_delete_task(self, client: TestClient, list_id: str):
        create_resp = client.post(
            f"/api/lists/{list_id}/tasks",
            json={"title": "Test Task"}
        )
        task_id = create_resp.json()["id"]

        delete_resp = client.delete(f"/api/lists/{list_id}/tasks/{task_id}")
        assert delete_resp.status_code == 204
        
        toggle_resp = client.patch(f"/api/lists/{list_id}/tasks/{task_id}/toggle")
        assert toggle_resp.status_code == 404