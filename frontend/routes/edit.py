from os import getenv
from flask import render_template, request, redirect, url_for
from requests import get, post, put
from flask_login import current_user
from .. import app, BACKEND_URL


@app.get("/edit_task/<int:task_id>")
def edit_task(task_id):
    response = get(f"{BACKEND_URL}/task/{task_id}")
    if response.status_code == 200:
        task = response.json()
        return render_template("edit.html", task=task, task_id=task_id)
    else:
        return f"Error {response.status_code}"


@app.post("/edit_task/<int:task_id>")
def update_task(task_id):
    data = {
        "id": task_id,
        'title': request.form.get('title'),
        "author": current_user.email,
        'content': request.form.get('content'),
        'deadline': request.form.get('deadline'),
        'theme': request.form.get('choice'),
        'importance': request.form.get('importance')
    }
    print(data)
    response = put(f"{BACKEND_URL}/edit_task", json=data)
    if response.status_code == 200:
        return redirect(url_for('index'))
    else:
        return f"Error {response.status_code}"
