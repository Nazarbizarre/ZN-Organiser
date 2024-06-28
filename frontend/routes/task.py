from os import getenv

from .. import app, BACKEND_URL

from flask import Flask, render_template, request, redirect, flash, url_for

from flask_login import current_user, login_required, LoginManager, login_user
from sqlalchemy import select
from requests import get, post
from frontend.db import Session, User
from datetime import datetime






@app.post("/add_task")
@login_required
def add_task():

    data = {
        "id": len(get(f"{BACKEND_URL}/get_tasks").json()) + 1,
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