import time
from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.list import ListSchema
from app.models.task import TaskSchema
from app.core.database import ListORM, TaskORM

class ListRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all_lists(self) -> list[ListSchema]:
        lists_orm = self.db.scalars(select(ListORM)).all()
        return [
            ListSchema(
                id=list_orm.id,
                title=list_orm.title,
                tasks=[
                    TaskSchema(
                        id=task.id,
                        title=task.title,
                        completed=task.completed,
                        createdAt=task.createdAt,
                        listId=task.listId
                    ) for task in list_orm.tasks
                ],
                createdAt=list_orm.createdAt
            ) for list_orm in lists_orm
        ]

    def create_list(self, title: str) -> ListSchema:
        new_list_orm = ListORM(
            id=str(uuid4()),
            title=title,
            tasks=[],
            createdAt=int(time.time())
        )
        self.db.add(new_list_orm)
        self.db.commit()
        self.db.refresh(new_list_orm)
        return ListSchema(
            id=new_list_orm.id,
            title=new_list_orm.title,
            tasks=new_list_orm.tasks,
            createdAt=new_list_orm.createdAt
        )

    def delete_list(self, list_id: str) -> bool:
        list_orm = self.db.get(ListORM, list_id)
        if not list_orm:
            return False
        self.db.delete(list_orm)
        self.db.commit()
        return True