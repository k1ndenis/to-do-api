from uuid import uuid4
import time

from app.repository.list_repository import ListRepository
from app.models.list import ListCreateSchema, ListSchema

class ListService:
    @staticmethod
    def get_all_lists() -> list[ListSchema]:
        return ListRepository.get_all_lists()

    @staticmethod
    def create_list(payload: ListCreateSchema) -> ListSchema:
        return ListRepository.create_list(title=payload.title)

    @staticmethod
    def delete_list(list_id: str) -> bool:
        return ListRepository.delete_list(list_id=list_id)