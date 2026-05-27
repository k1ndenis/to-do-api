from uuid import uuid4
import time
from sqlalchemy.orm import Session

from app.repository.list_repository import ListRepository
from app.models.list import ListCreateSchema, ListSchema

class ListService:
    @staticmethod
    def get_all_lists(db: Session) -> list[ListSchema]:
        return ListRepository.get_all_lists(db)

    @staticmethod
    def create_list(db: Session, payload: ListCreateSchema) -> ListSchema:
        return ListRepository.create_list(db, title=payload.title)

    @staticmethod
    def delete_list(db: Session, list_id: str) -> bool:
        return ListRepository.delete_list(db, list_id)