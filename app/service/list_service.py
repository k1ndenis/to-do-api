from uuid import uuid4
import time
from sqlalchemy.orm import Session

from app.repository.list_repository import ListRepository
from app.models.list import ListCreateSchema, ListSchema
from app.cache.redis import RedisCacheBackend

class ListService:
    def __init__(self,
        db: Session,
        cache_redis_url: str,
        cache_ttl_seconds: int,
        cache_key: str
    ) -> None:
        self.db = db
        self.repository = ListRepository(db)
        self.cache = RedisCacheBackend(cache_redis_url, cache_ttl_seconds)
        self.cache_key = cache_key

    def get_all_lists(self) -> list[ListSchema]:
        cached_lists = self.cache.get(self.cache_key)
        if cached_lists:
            return [ListSchema(**item) for item in cached_lists]
        
        lists = self.repository.get_all_lists()

        lists_dicts = [item.model_dump() for item in lists]
        self.cache.set(self.cache_key, lists_dicts)

        return lists

    def create_list(self, payload: ListCreateSchema) -> ListSchema:
        self.cache.delete(self.cache_key)
        return self.repository.create_list(title=payload.title)

    def delete_list(self, list_id: str) -> bool:
        self.cache.delete(self.cache_key)
        return self.repository.delete_list(list_id)