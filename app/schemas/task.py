from pydantic import BaseModel

class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool = False
    createdAt: int
    listId: str

class TaskCreateSchema(BaseModel):
    title: str