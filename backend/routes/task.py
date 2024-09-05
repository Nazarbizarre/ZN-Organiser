from ..main import app
from sqlalchemy import select, update
from datetime import datetime
from fastapi import HTTPException
from ..db import Session, Task
from ..schemas import TaskData, UserTasks, DeleteTaskRequest



@app.get("/get_tasks")
def get_tasks():
    with Session.begin() as session:
        tasks = session.scalars(select(Task)).all()
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
def delete_task(data: DeleteTaskRequest):
    with Session.begin() as session:
        task = session.get(Task, data.id)
        if not task:
            raise HTTPException(status_code=404, detail="Not found")
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
            importance=data.importance
        )
        session.execute(upd)
        return task