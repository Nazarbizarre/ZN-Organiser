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
    completed: Optional[bool] = False


class UserTasks(BaseModel):
    email: str
    completed: bool


class TaskGetRequest(BaseModel):
    id: int
    user: str

class TaskTheme(BaseModel):
    email: str
    theme: str


class FilterData(BaseModel):
    email: str
    start_date: str
    end_date: str


class AlertData(BaseModel):
    email: str
    now: str
    tomorrow: str