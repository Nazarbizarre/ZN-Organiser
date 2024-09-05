
from .. import app
from flask import render_template
from requests import get
from os import getenv
BACKEND_URL = getenv("BACKEND_URL")

@app.get("/")
def index():
    tasks = {
        "tasks":get(f"{BACKEND_URL}/get_tasks").json()
    }
    nickname = current.split("@")[0]
    return render_template("main.html", **tasks, nickname=nickname)