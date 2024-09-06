from .. import app
from flask import render_template, request
from requests import get
from flask_login import current_user, login_required
from os import getenv
BACKEND_URL = getenv("BACKEND_URL")
from datetime import datetime


@login_required
@app.get("/calendar_form")
def calendar_get():
    date_t = datetime.now().strftime("%d/%m/%Y")
    return render_template("calendar_form.html", date_t=date_t)


@login_required
@app.post("/calendar")
def calendar_post():
    response = request.form.get("response")
    current = current_user.email
    print(current)
    data = {
        "email": current,
        "start_date": response.get("start_date"),
        "end_date": response.get("end_date")
    }
    filtered_tasks = {
        "filtered_tasks":get(f"{BACKEND_URL}/calendar", json=data).json()
    }
    nickname = current.split("@")[0]
    return render_template("calendar.html", **filtered_tasks, nickname=nickname)



