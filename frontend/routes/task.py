from os import getenv

from .. import app, BACKEND_URL

from flask import render_template, request, redirect, url_for

from flask_login import login_required, current_user

from requests import get, post

from datetime import datetime






@app.post("/add_task")
@login_required
def add_task():
    current = current_user.email
    print(current)
    data = {
        "id": len(get(f"{BACKEND_URL}/tasks_list").json()) + 1,
        "author": current,
        "title": request.form.get('title'),
        "content": request.form.get('content'),
        "published": datetime.now().isoformat(),
        "deadline": request.form.get('deadline')
    }


    task = post(f"{BACKEND_URL}/add_task", json=data)
    if task.status_code == 200:
        return redirect(url_for("index"))
    return(f"Error {task.status_code}")

 
 
@app.get('/add_task')
@login_required
def get_create_task():
    return render_template("create_task.html")