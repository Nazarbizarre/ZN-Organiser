from pydantic import BaseModel, ConfigDict

from datetime import datetime


class TaskData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int

    title: str
    content: str
    published: datetime
    deadline: datetime

