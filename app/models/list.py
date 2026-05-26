from pydantic import BaseModel
from typing import List

class ListSchema(BaseModel):
    id: str
    title: str
    tasks: List['TaskSchema'] = []
    createdAt: int

class ListCreateSchema(BaseModel):
    title: str

from .task import TaskSchema