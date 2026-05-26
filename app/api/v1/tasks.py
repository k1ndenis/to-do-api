from fastapi import APIRouter, HTTPException
from app.service.task_service import TaskService
from app.models.task import TaskCreateSchema, TaskSchema

router = APIRouter()

@router.post("/lists/{list_id}/tasks")
def create_task(list_id: str, payload: TaskCreateSchema) -> TaskSchema:
    return TaskService.create_task(list_id=list_id, payload=payload)

@router.delete("/lists/{list_id}/tasks/{task_id}")
def delete_task(list_id: str, task_id: str):
    success = TaskService.delete_task(list_id=list_id, task_id=task_id)
    if success:
        return {"message": "Task deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="List or task not found")

@router.patch("/lists/{list_id}/tasks/{task_id}/toggle")
def toggle_task_completion(list_id: str, task_id: str) -> TaskSchema:
    return TaskService.toggle_task_completion(list_id=list_id, task_id=task_id)