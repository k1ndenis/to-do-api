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
        self.repository = ListRepository(
            db=db,
            cache_redis_url=cache_redis_url,
            cache_ttl_seconds=cache_ttl_seconds,
            cache_lists_key=cache_key
        )
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

    def create_list(db: Session, payload: ListCreateSchema) -> ListSchema:
        return ListRepository.create_list(db, title=payload.title)

    def delete_list(db: Session, list_id: str) -> bool:
        return ListRepository.delete_list(db, list_id)