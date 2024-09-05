from .. import app,BACKEND_URL
from flask import render_template, redirect, url_for,request
from requests import delete

@app.get("/done/<int:task_id>")
def done_validator(task_id):
    return render_template("delete.html", task_id = task_id)

@app.post("/done/<int:task_id>")
def done(task_id):
    response = request.form.get("response")
    if response == "yes":
        print("yes")
        response = delete(f"{BACKEND_URL}/delete_task", json={"id": task_id})
        if response.status_code == 200:
            return redirect(url_for("index"))
        else:
            return f"Error {response.status_code}"
    if response == "no":
        return redirect(url_for("product" , task_id=task_id))