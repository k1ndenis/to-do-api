from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Generator
import os

from app.core.database import SessionLocal
from app.service.list_service import ListService
from app.service.task_service import TaskService

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_list_service(db: Session = Depends(get_db)) -> ListService:
    redis_url = os.getenv("REDIS_URL")
    return ListService(
        db=db,
        cache_redis_url=redis_url,
        cache_ttl_seconds=60,
        cache_key="all_lists"
    )

def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    return TaskService(db=db)