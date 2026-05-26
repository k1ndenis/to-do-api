from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uuid import uuid4
import time

from app.schemas.task import TaskSchema, TaskCreateSchema
from app.schemas.list import ListSchema, ListCreateSchema

app = FastAPI(title="To-Do API",
    description="API для управления to-do списками",
    version="1.0.0",
    contact={"name": "Denis", "email": "k1ndenis.dev@gmail.com"})

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

lists: list[ListSchema] = []

@app.get("/api/lists")
def read_lists():
    return lists

@app.post("/api/lists")
def create_list(payload: ListCreateSchema) -> ListSchema:
    new_list: ListSchema = ListSchema(
        id=str(uuid4()),
        title=payload.title,
        tasks=[],
        createdAt=int(time.time())
    )
    lists.append(new_list)
    return new_list

@app.delete("/api/lists/{list_id}")
def delete_list(list_id: str):
    global lists
    lists = [l for l in lists if l.id != list_id]
    return {"message": "List deleted successfully"}

@app.post("/api/lists/{list_id}/tasks")
def create_task(list_id: str, payload: TaskCreateSchema) -> TaskSchema:
    new_task: TaskSchema = TaskSchema(
        id=str(uuid4()),
        title=payload.title,
        completed=False,
        createdAt=int(time.time())
    )
    for l in lists:
        if l.id == list_id:
            l.tasks.append(new_task)
            return new_task
    return {"message": "List not found"}

@app.delete("/api/lists/{list_id}/tasks/{task_id}")
def delete_task(list_id: str, task_id: str):
    for l in lists:
        if l.id == list_id:
            l.tasks = [t for t in l.tasks if t.id != task_id]
            return {"message": "Task deleted successfully"}
    return {"message": "List not found"}

@app.patch("/api/lists/{list_id}/tasks/{task_id}/toggle")
def toggle_task_completion(list_id: str, task_id: str) -> TaskSchema:
    for l in lists:
        if l.id == list_id:
            for t in l.tasks:
                if t.id == task_id:
                    t.completed = not t.completed
                    return t
    raise HTTPException(status_code=404, detail="List or task not found")   
    