from pydantic import BaseModel

class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool = False
    createdAt: int

class TaskCreateSchema(BaseModel):
    title: str