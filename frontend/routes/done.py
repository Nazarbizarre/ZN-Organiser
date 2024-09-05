from .. import app,BACKEND_URL
from flask import render_template, redirect, url_for, request
from flask_login import current_user
from requests import delete


@app.get("/done/<int:task_id>")
def done(task_id):
    response = delete(f"{BACKEND_URL}/delete_task", json={"id": task_id, "user": current_user.email})
    if response.status_code == 200:
        return redirect(url_for("index"))
    else:
         return f"Error {response.status_code}"
    