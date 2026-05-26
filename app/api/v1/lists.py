from fastapi import APIRouter, HTTPException
from app.service.list_service import ListService
from app.models.list import ListCreateSchema, ListSchema

router = APIRouter()

@router.get("/lists")
def read_lists():
    return ListService.get_all_lists()

@router.post("/lists")
def create_list(payload: ListCreateSchema) -> ListSchema:
    return ListService.create_list(payload=payload)

@router.delete("/lists/{list_id}")
def delete_list(list_id: str):
    success = ListService.delete_list(list_id=list_id)
    if success:
        return {"message": "List deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="List not found")