from uuid import uuid4
import time 
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repository.list_repository import ListRepository
from app.repository.task_repository import TaskRepository
from app.models.task import TaskCreateSchema, TaskSchema

class TaskService:
    @staticmethod
    def create_task(db: Session, list_id: str, payload: TaskCreateSchema) -> TaskSchema:
        try:
            return TaskRepository.create_task(db, list_id, payload.title)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    @staticmethod
    def delete_task(db: Session, list_id: str, task_id: str) -> bool:
        try:
            return TaskRepository.delete_task(db, list_id, task_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    @staticmethod
    def toggle_task_completion(db: Session, list_id: str, task_id: str) -> TaskSchema:
        try:
            return TaskRepository.toggle_task_completion(db, list_id, task_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))