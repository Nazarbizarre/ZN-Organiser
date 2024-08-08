from main import app
from sqlalchemy import select
from datetime import datetime
from db import Session, Task
from schemas import TaskData, UserTasks




@app.get("/get_tasks")
def get_tasks(data: UserTasks):
    with Session.begin() as session:
        tasks = session.scalars(select(Task).where(Task.author == data.email)).all()
        tasks = [TaskData.model_validate(task) for task in tasks]
        return tasks


@app.get("/task/{task_id}")
def get_task(task_id):
    with Session.begin() as session:
        task = session.scalar(select(Task).where(Task.id == task_id))
        task = TaskData.model_validate(task)
        return task


@app.post("/add_task")
def add_task(data: TaskData):
    with Session.begin() as session:
        task = Task(**data.model_dump())
        session.add(task)
        return task