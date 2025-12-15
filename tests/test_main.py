import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import TaskStatus


client = TestClient(app)


def test_get_status() -> None:
    """Test the /status endpoint."""
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_all_tasks() -> None:
    """Test the /tasks endpoint."""
    response = client.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert isinstance(tasks, list)
    assert len(tasks) > 0


def test_get_productivity_report() -> None:
    """Test the /report endpoint."""
    response = client.get("/report")
    assert response.status_code == 200
    report = response.json()
    assert "total_tasks" in report
    assert "completed_tasks" in report
    assert "total_hours_spent" in report
    assert "completion_rate" in report


def test_log_task() -> None:
    """Test the /log_task endpoint."""
    new_task = {
        "task_id": 0,
        "title": "Test task",
        "status": TaskStatus.IN_PROGRESS,
        "hours_spent": 5.0,
    }
    response = client.post("/log_task", json=new_task)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Task ID" in data["message"]
