
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.tasks import create_task, complete_task

app = FastAPI(title="Task Tracker API")
tasks: list[dict] = []

origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

frontend_origin = os.getenv("FRONTEND_ORIGIN")
if frontend_origin:
    origins.append(frontend_origin.rstrip("/"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=["Content-Type"],
)


class TaskInput(BaseModel):
    title: str = Field(min_length=1, max_length=100)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/tasks")
def get_tasks():
    return tasks


@app.post("/api/tasks", status_code=201)
def add_task(payload: TaskInput):
    try:
        return create_task(tasks, payload.title)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.patch("/api/tasks/{task_id}/complete")
def mark_complete(task_id: int):
    task = complete_task(tasks, task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task
