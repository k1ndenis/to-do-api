from fastapi import APIRouter, HTTPException, status, Depends
from app.service.list_service import ListService
from app.models.list import ListCreateSchema, ListSchema
from sqlalchemy.orm import Session

from app.dependency import get_db

router = APIRouter()

@router.get("/lists")
def read_lists(db: Session = Depends(get_db)) -> list[ListSchema]:
    service = ListService(
        db=db,
        cache_redis_url="redis://localhost:6379",
        cache_ttl_seconds=60,
        cache_key="all_lists"
    )
    return service.get_all_lists()

@router.post("/lists", status_code=status.HTTP_201_CREATED)
def create_list(payload: ListCreateSchema, db: Session = Depends(get_db)) -> ListSchema:
    return ListService.create_list(db, payload)

@router.delete("/lists/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_list(list_id: str, db: Session = Depends(get_db)):
    success = ListService.delete_list(db, list_id)
    if success:
        return {"message": "List deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="List not found")