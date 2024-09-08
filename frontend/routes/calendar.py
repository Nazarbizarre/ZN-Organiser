from .. import app
from flask import render_template, request
from requests import get
from flask_login import current_user, login_required
from os import getenv
BACKEND_URL = getenv("BACKEND_URL")
from datetime import datetime


@login_required
@app.get("/calendar")
def calendar_get():
    date_t = datetime.now().strftime("%d/%m/%Y")
    return render_template("calendar.html", date_t=date_t)


@login_required
@app.post("/calendar")
def calendar_post():
    current = current_user.email
    print(current)
    start_date_str = request.form.get("start-date")
    end_date_str = request.form.get("end-date")

    if start_date_str and end_date_str:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")  
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    else:
        return "Start date and End date are required.", 400

    # formatted_start_date = start_date.strftime("%d/%m/%Y")
    # formatted_end_date = end_date.strftime("%d/%m/%Y")
    data = {
        "email": current,
        "start_date": start_date,
        "end_date": end_date
    }
    print(data)
    filtered_tasks = {
        "filtered_tasks":get(f"{BACKEND_URL}/filters", json=data).json()
    }
    print(filtered_tasks)
    tasks = filtered_tasks["filtered_tasks"]
    print(tasks)
    nickname = current.split("@")[0]
    return render_template("calendar.html", filtered_tasks=tasks, nickname=nickname)


