from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class TaskData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None
    author: str
    title: str
    content: str
    published: datetime
    deadline: datetime

