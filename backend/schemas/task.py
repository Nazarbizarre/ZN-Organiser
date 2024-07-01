from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class TaskData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    author: str
    title: str
    content: str
    published: datetime
    deadline: datetime

class UserTasks(BaseModel):
    id: Optional[int] = None
    email: str