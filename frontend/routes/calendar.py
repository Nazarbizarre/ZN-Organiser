from .. import app
from flask import render_template, request, redirect, url_for
from requests import get
from flask_login import current_user, login_required
from os import getenv
BACKEND_URL = getenv("BACKEND_URL")
from datetime import datetime

def sort_dates(dates): # ??? 
    # Define a key function that converts a date string to a datetime object
    def date_key(date_string):
        return datetime.strptime(date_string, "%d/%m/%Y")
     
    # Use the sorted function to sort the list of dates, using the date_key function as the key
    return sorted(dates, key=date_key)

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
    end_date_str = request.form.get("end-date")
    if not end_date_str:
        return redirect(url_for("calendar_get"))
    start_date_str = request.form.get("start-date")
    if not start_date_str:
        return redirect(url_for("calendar_get"))
    data = {
        "email": current,
        "start_date": start_date_str,
        "end_date": end_date_str
    }
    print(data)

    filtered_tasks = get(f"{BACKEND_URL}/filters", json=data).json()
    print(filtered_tasks)
    # filtered_tasks.sort(key = lambda date: datetime.strptime(date, "%d-%m-%Y"))
    # filtered_tasks = sort_dates(filtered_tasks)
    sorted_tasks = sorted(filtered_tasks, key=lambda x: datetime.strptime(x['deadline'], "%Y-%m-%d"))

    nickname = current.split("@")[0]
    return render_template("calendar.html", filtered_tasks=sorted_tasks, nickname=nickname, start_date=start_date_str, end_date=end_date_str)

