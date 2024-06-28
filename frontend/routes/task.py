from os import getenv

from .. import app

from flask import Flask, render_template, request, redirect, flash, url_for

from flask_login import current_user, login_required, LoginManager, login_user
from sqlalchemy import select
from requests import get, post
from frontend.db import Session, User
from datetime import datetime



BACKEND_URL = getenv("BACKEND_URL")


@app.post("/add_task")
@login_required
def add_task():

    data = {
        "id": len(get(f"{BACKEND_URL}/add_task").json()) + 1,
        "title": request.form['title'],
        "content": request.form['content'],
        "published": datetime.now().isoformat(),
        "deadline": request.form['deadline']

    }
    

    task = post(f"{BACKEND_URL}/add_task", json=data)
    if task.status_code == 200:
        return redirect(url_for("index"))
    return(f"Error {task.status_code}")

 
 
@app.get('/add_task')
@login_required
def get_create_task():
    return render_template("create_task.html")