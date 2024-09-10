from flask import render_template, request
from requests import get
from flask_login import current_user, login_required
from .. import app, BACKEND_URL
from datetime import datetime


@app.get("/board")
@login_required
def board():
    current = current_user.email
    data = {
        "email": current,
        "completed": False
    }
    tasks =  get(f"{BACKEND_URL}/get_tasks", json=data).json()
    print(tasks)
    nickname = current.split("@")[0]
    return render_template("board.html", tasks=tasks, nickname=nickname)

