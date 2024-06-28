import app
from sqlalchemy import select
from datetime import datetime
from db import Session, Task
from schemas import TaskData


# from fastapi.exceptions import HTTPException

@app.post("/add_task")
def add_task(data: TaskData):
    with Session.begin() as session:
        task = Task(**data.model_dump())
        session.add(task)
        return task