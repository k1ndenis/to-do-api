import time
from uuid import uuid4

from app.core.database import lists_db
from app.models.list import ListSchema

class ListRepository:
    @staticmethod
    def get_all_lists() -> list[ListSchema]:
        return lists_db

    @staticmethod
    def create_list(title: str) -> ListSchema:
        new_list = ListSchema(
            id=str(uuid4()),
            title=title,
            tasks=[],
            createdAt=int(time.time())
        )
        lists_db.append(new_list)
        return new_list

    @staticmethod
    def delete_list(list_id: str) -> bool:
        global lists_db
        initial_length = len(lists_db)
        lists_db = [l for l in lists_db if l.id != list_id]
        return len(lists_db) < initial_length