from main import app
from sqlalchemy import select
from datetime import datetime
from db import Session, Task
from schemas import TaskData, UserTasks


from fastapi.exceptions import HTTPException

@app.get("/get_tasks")
def get_tasks(data: UserTasks):
    with Session.begin() as session:
        tasks = session.scalars(select(Task).where(Task.author == data.email)).all()
        tasks = [TaskData.model_validate(task) for task in tasks]
        return tasks


@app.get("/task")
def get_task(data: UserTasks):
    with Session.begin() as session:
        task = session.scalar(select(Task).where(Task.id == data.id).where(Task.author == data.email))
        if task:
            task = TaskData.model_validate(task)
            return task
        else:
            raise HTTPException(status_code=403, detail="Permission denied")
            

@app.post("/add_task")
def add_task(data: TaskData):
    with Session.begin() as session:
        task = Task(**data.model_dump())
        session.add(task)
        return task
    
@app.get("/tasks_list")
def tasks_list():
    with Session.begin() as session:
        tasks = session.scalars(select(Task)).all()
        tasks = [TaskData.model_validate(task) for task in tasks]
        return tasks
