
from .. import app
from flask import render_template
from flask_login import current_user, login_required
from requests import get
from os import getenv
BACKEND_URL = getenv("BACKEND_URL")

@app.get("/")
@login_required
def index():
    current = current_user.email
    print(current)
    data = {
        "email": current,
        "completed": False
    }
    tasks = {
        "tasks":get(f"{BACKEND_URL}/get_tasks", json=data).json()
    }
    nickname = current.split("@")[0]
    return render_template("main.html", **tasks, nickname=nickname)