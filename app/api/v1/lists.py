from fastapi import APIRouter, HTTPException, status, Depends
from app.service.list_service import ListService
from app.models.list import ListCreateSchema, ListSchema
from sqlalchemy.orm import Session

from app.dependency import get_db, get_list_service

router = APIRouter()

@router.get("/lists")
def read_lists(list_service: ListService = Depends(get_list_service)) -> list[ListSchema]:
    return list_service.get_all_lists()

@router.post("/lists", status_code=status.HTTP_201_CREATED)
def create_list(payload: ListCreateSchema, list_service: ListService = Depends(get_list_service)) -> ListSchema:
    return list_service.create_list(payload)

@router.delete("/lists/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_list(list_id: str, list_service: ListService = Depends(get_list_service)):
    success = list_service.delete_list(list_id)
    if success:
        return {"message": "List deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="List not found")