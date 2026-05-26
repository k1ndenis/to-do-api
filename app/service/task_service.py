from uuid import uuid4
import time 
from fastapi import HTTPException

from app.repository.list_repository import ListRepository
from app.repository.task_repository import TaskRepository
from app.models.task import TaskCreateSchema, TaskSchema

class TaskService:
    @staticmethod
    def create_task(list_id: str, payload: TaskCreateSchema) -> TaskSchema:
        try:
            return TaskRepository.create_task(list_id=list_id, title=payload.title)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    @staticmethod
    def delete_task(list_id: str, task_id: str) -> bool:
        try:
            return TaskRepository.delete_task(list_id=list_id, task_id=task_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    @staticmethod
    def toggle_task_completion(list_id: str, task_id: str) -> TaskSchema:
        try:
            return TaskRepository.toggle_task_completion(list_id=list_id, task_id=task_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))