from os import getenv
from flask import render_template, request, redirect, url_for
from requests import get, post, put
from .. import app

BACKEND_URL = getenv("BACKEND_URL")

@app.get("/edit_task/<int:task_id>")
def edit_task(task_id):
    response = put(f"{BACKEND_URL}/edit_task/{task_id}")
    if response.status_code == 200:
        task = response.json()
        return render_template("edit.html", task=task, task_id=task_id)
    else:
        return f"Error {response.status_code}"

@app.post("/edit_task/<int:task_id>")
def update_task(task_id):
    data = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'deadline': request.form.get('deadline'),
        'choice': request.form.get('choice'),
        'importance': request.form.get('importance')
    }

    

    response = put(f"{BACKEND_URL}/edit_task/{task_id}", json=data)

    if response.status_code == 200:
        return redirect(url_for('index'))
    else:
        return f"Error {response.status_code}"
