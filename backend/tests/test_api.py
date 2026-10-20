
import pytest
from fastapi.testclient import TestClient

from app.main import app, tasks

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_tasks():
    tasks.clear()
    yield
    tasks.clear()


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_task():
    response = client.post(
        "/api/tasks",
        json={"title": "Learn APIs"},
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "title": "Learn APIs",
        "completed": False,
    }


def test_empty_title_is_rejected():
    response = client.post(
        "/api/tasks",
        json={"title": "   "},
    )

    assert response.status_code == 400


def test_invalid_input_is_rejected():
    response = client.post(
        "/api/tasks",
        json={"title": ""},
    )

    assert response.status_code == 422


def test_complete_task():
    created = client.post(
        "/api/tasks",
        json={"title": "Practice testing"},
    )
    task_id = created.json()["id"]

    response = client.patch(
        f"/api/tasks/{task_id}/complete"
    )

    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_missing_task_returns_404():
    response = client.patch("/api/tasks/999/complete")

    assert response.status_code == 404


def test_task_is_returned_by_list_endpoint():
    client.post("/api/tasks", json={"title": "Integration test"})

    response = client.get("/api/tasks")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Integration test"
