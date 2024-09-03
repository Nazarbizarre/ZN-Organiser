from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date


class TaskData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None
    author: str
    title: str
    content: str
    published: str
    deadline: str
    theme: str
    importance: str

class UserTasks(BaseModel):
    email: str


class TaskEdit(BaseModel):
    title: str
    content: str
    deadline: str
    theme: str
    importance: str