from ..main import app
from sqlalchemy import select, update, and_
from datetime import datetime
from fastapi import HTTPException
from ..db import Session, Task
from ..schemas import TaskData, UserTasks, TaskGetRequest, TaskTheme



@app.get("/get_tasks")
def get_tasks(data: UserTasks):
    with Session.begin() as session:
        tasks = session.scalars(select(Task).where(Task.author == data.email).where(Task.completed == data.completed)).all()
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


@app.delete("/delete_task")
def delete_task(data: TaskGetRequest):
    with Session.begin() as session:
        task = session.scalar(select(Task).where(Task.id == data.id))
        if not task:
            raise HTTPException(status_code=404, detail="Not found")
        if task.author != data.user:
            raise HTTPException(status_code=403, detail="Permission denied")
        session.delete(task)
        return {"message": "Task deleted successfully"}



@app.put("/edit_task")
def edit_task(data: TaskData):
    with Session.begin() as session:
        task = session.scalar(select(Task).where(Task.id == data.id))
        if task.author != data.author:
            raise HTTPException(status_code=403, detail="Permission denied")
        upd = update(Task).where(Task.id == data.id).values(
            title=data.title,
            content=data.content,
            deadline=data.deadline,
            theme=data.theme,
            importance=data.importance,
            completed=False
        )
        session.execute(upd)
        return task
    
@app.post("/task_done")
def task_done(data: TaskGetRequest):
    with Session.begin() as session:
        task = session.scalar(select(Task).where(Task.id == data.id))
        if not task:
            raise HTTPException(status_code=404, detail="Not found")
        if task.author != data.user:
            raise HTTPException(status_code=403, detail="Permission denied")
        upd = update(Task).where(Task.id == data.id).values(
            completed=True
        )
        session.execute(upd)
        return task

@app.get("/themes")
def themes(data: TaskTheme):
    with Session.begin() as session:
        selected_tasks = session.scalars(select(Task).where(and_(Task.theme == data.theme), Task.author == data.email)).all()
        selected_tasks = [TaskData.model_validate(task) for task in selected_tasks]
        return selected_tasks