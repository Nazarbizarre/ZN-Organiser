from .. import app, BACKEND_URL
from flask import render_template
from requests import get
from flask_login import current_user, login_required
from os import getenv


@app.get("/completed_tasks")
@login_required
def completed():
    current = current_user.email
    print(current)
    data = {
        "email": current,
        "completed": True
    }
    tasks = {
        "tasks":get(f"{BACKEND_URL}/get_tasks", json=data).json()
    }
    nickname = current.split("@")[0]
    return render_template("completed.html", **tasks, nickname=nickname)