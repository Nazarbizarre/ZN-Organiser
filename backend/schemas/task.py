from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class TaskData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None
    author: str
    title: str
    content: str
    published: Optional[str] = datetime.now().date().isoformat()
    deadline: str
    theme: str
    importance: str

class UserTasks(BaseModel):
    email: str


class DeleteTaskRequest(BaseModel):
    id: int