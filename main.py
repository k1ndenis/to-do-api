from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uuid import uuid4
import time

from schemas.task import TaskSchema, TaskCreateSchema
from schemas.list import ListSchema, ListCreateSchema

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

lists: list[ListSchema] = []

tasks: list[TaskSchema] = [
    TaskSchema(
        id='1',
        title="Task 1",
        completed=False,
        createdAt=1,
        listId="1",
    ),
    TaskSchema(
        id='2',
        title="Task 2",
        completed=False,
        createdAt=2,
        listId="1"
    ),
    TaskSchema(
        id='3',
        title="Task 3",
        completed=False,
        createdAt=3,
        listId="1"
    )
]

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


@app.get("/api/tasks")
def read_tasks():
    return tasks

@app.post("/api/tasks")
def create_task(payload: TaskCreateSchema) -> TaskSchema:
    new_task = TaskSchema(
        id=str(uuid4()),
        title=payload.title,
        completed=False,
        createdAt=int(time.time()),
        listId="1",
    )

    tasks.append(new_task)
    return new_task