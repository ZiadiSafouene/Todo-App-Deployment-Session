
def create_task(tasks: list[dict], title: str) -> dict:
    title = title.strip()

    if not title:
        raise ValueError("Task title cannot be empty")

    next_id = max((task["id"] for task in tasks), default=0) + 1

    task = {
        "id": next_id,
        "title": title,
        "completed": False,
    }
    tasks.append(task)
    return task


def complete_task(tasks: list[dict], task_id: int) -> dict | None:
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            return task

    return None
