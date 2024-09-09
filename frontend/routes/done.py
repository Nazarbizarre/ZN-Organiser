from .. import app,BACKEND_URL
from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_required
from requests import post


@app.get("/done/<int:task_id>")
@login_required
def done(task_id):
    response = post(f"{BACKEND_URL}/task_done", json={"id": task_id, "user": current_user.email})
    if response.status_code == 200:
        return redirect(url_for("index"))
    else:
         return f"Error {response.status_code}"
    