from uuid import uuid4
import time 
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repository.list_repository import ListRepository
from app.repository.task_repository import TaskRepository
from app.models.task import TaskCreateSchema, TaskSchema

class TaskService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = TaskRepository(db=db)

    def create_task(self, list_id: str, payload: TaskCreateSchema) -> TaskSchema:
        try:
            return self.repository.create_task(list_id, payload.title)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    def delete_task(self, list_id: str, task_id: str) -> bool:
        try:
            return self.repository.delete_task(list_id, task_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    def toggle_task_completion(self, list_id: str, task_id: str) -> TaskSchema:
        try:
            return self.repository.toggle_task_completion(list_id, task_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))