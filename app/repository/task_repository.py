from app.core.database import lists_db
from app.models.task import TaskSchema
from uuid import uuid4
import time

class TaskRepository:
    @staticmethod
    def create_task(list_id: str, title: str) -> TaskSchema:
        new_task = TaskSchema(
            id=str(uuid4()),
            title=title,
            completed=False,
            createdAt=int(time.time())
        )
        for l in lists_db:
            if l.id == list_id:
                l.tasks.append(new_task)
                return new_task
        raise ValueError("List not found")

    @staticmethod
    def delete_task(list_id: str, task_id: str) -> bool:
        for l in lists_db:
            if l.id == list_id:
                initial_length = len(l.tasks)
                l.tasks = [t for t in l.tasks if t.id != task_id]
                return len(l.tasks) < initial_length
        raise ValueError("List not found")

    @staticmethod
    def toggle_task_completion(list_id: str, task_id: str) -> TaskSchema:
        for l in lists_db:
            if l.id == list_id:
                for t in l.tasks:
                    if t.id == task_id:
                        t.completed = not t.completed
                        return t
        raise ValueError("List or Task not found")