from .. import app,BACKEND_URL
from flask import render_template, redirect, url_for,request
from requests import delete
from flask_login import current_user, login_required
from requests import get


@app.get("/delete_task/<int:task_id>")
@login_required
def delete_validator(task_id):
    return render_template("delete.html", task_id = task_id)


@app.post("/delete_task/<int:task_id>")
@login_required
def delete_task(task_id):
    response = request.form.get("response")
    tasks_response = get(f"{BACKEND_URL}/task/{task_id}")
    redirect_pos = "index"
    if tasks_response.status_code == 200:
        selected_product = tasks_response.json()
        if selected_product.get("completed") == True:
            redirect_pos = "completed"
    if response == "yes":
        print("yes")
        response = delete(f"{BACKEND_URL}/delete_task", json={"id": task_id,"user": current_user.email})
        if response.status_code == 200:
            return redirect(url_for(redirect_pos))
        else:
            return f"Error {response.status_code}"
    if response == "no":
        return redirect(url_for("product" , product_id=task_id))