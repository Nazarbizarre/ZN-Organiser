
from .. import app
from flask import render_template
from requests import get
from flask_login import current_user, login_required
from os import getenv
BACKEND_URL = getenv("BACKEND_URL")

@app.get("/board")
@login_required
def board():
    current = current_user.email
    data = {
        "email": current
    }
    tasks = {
        "tasks":get(f"{BACKEND_URL}/get_tasks", json=data).json()
    }
    nickname = current.split("@")[0]
    return render_template("board.html", **tasks, nickname=nickname)