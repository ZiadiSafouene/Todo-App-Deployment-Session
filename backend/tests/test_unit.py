
import pytest

from app.tasks import create_task, complete_task


def test_create_task_assigns_id_and_defaults():
    tasks = [{"id": 1, "title": "Existing", "completed": False}]

    result = create_task(tasks, "Learn pytest and ci cd")

    assert result == {
        "id": 2,
        "title": "Learn pytest and ci cd",
        "completed": False,
    }
    assert len(tasks) == 2


def test_create_task_trims_whitespace():
    tasks = []

    result = create_task(tasks, "  Learn testing  ")

    assert result["title"] == "Learn testing"


def test_create_task_rejects_empty_title():
    with pytest.raises(ValueError):
        create_task([], "   ")


def test_complete_task_changes_status():
    tasks = [{"id": 1, "title": "Test", "completed": False}]

    result = complete_task(tasks, 1)

    assert result["completed"] is True


def test_complete_missing_task_returns_none():
    assert complete_task([], 99) is None
