from app.models.task import TaskSchema
from uuid import uuid4
import time
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import ListORM, TaskORM

class TaskRepository:
    @staticmethod
    def create_task(db: Session, list_id: str, title: str) -> TaskSchema:
        list_orm = db.get(ListORM, list_id)
        if not list_orm:
            raise ValueError(f"List with id {list_id} not found")

        new_task_orm = TaskORM(
            id=str(uuid4()),
            title=title,
            completed=False,
            createdAt=int(time.time()),
            listId=list_id
        )
        db.add(new_task_orm)
        db.commit()
        db.refresh(new_task_orm)
        return TaskSchema(
            id=new_task_orm.id,
            title=new_task_orm.title,
            completed=new_task_orm.completed,
            createdAt=new_task_orm.createdAt
        )

    @staticmethod
    def delete_task(db: Session, list_id: str, task_id: str) -> bool:
        task = db.execute(
            select(TaskORM).where(
                TaskORM.id == task_id,
                TaskORM.listId == list_id
            )
        ).scalar_one_or_none()

        if not task:
            return False
        db.delete(task)
        db.commit()
        return True

    @staticmethod
    def toggle_task_completion(db: Session, list_id: str, task_id: str) -> TaskSchema:
        task = db.execute(
            select(TaskORM).where(
                TaskORM.id == task_id,
                TaskORM.listId == list_id
            )
        ).scalar_one_or_none()

        if not task:
            raise ValueError(f"Task with id {task_id} not found in list {list_id}")

        task.completed = not task.completed
        db.commit()
        db.refresh(task)
        return TaskSchema(
            id=task.id,
            title=task.title,
            completed=task.completed,
            createdAt=task.createdAt
        )