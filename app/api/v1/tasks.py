from fastapi import APIRouter, HTTPException, status, Depends

from app.service.task_service import TaskService
from app.models.task import TaskCreateSchema, TaskSchema
from app.dependency import get_db

router = APIRouter()

@router.post("/lists/{list_id}/tasks", status_code=status.HTTP_201_CREATED)
def create_task(list_id: str, payload: TaskCreateSchema, db: Session = Depends(get_db)) -> TaskSchema:
    return TaskService.create_task(db, list_id, payload)

@router.delete("/lists/{list_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(list_id: str, task_id: str, db: Session = Depends(get_db)):
    success = TaskService.delete_task(db, list_id, task_id)
    if success:
        return {"message": "Task deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="List or task not found")

@router.patch("/lists/{list_id}/tasks/{task_id}/toggle")
def toggle_task_completion(list_id: str, task_id: str, db: Session = Depends(get_db)) -> TaskSchema:
    return TaskService.toggle_task_completion(db, list_id, task_id)