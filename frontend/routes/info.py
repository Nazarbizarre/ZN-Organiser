

from .. import app, BACKEND_URL

from flask import render_template

from flask_login import login_required, current_user

from requests import get, post



@app.get("/task/<int:product_id>")
@login_required
def product(product_id):
    data = {
        "id": product_id,
        "email": current_user.email
    }                    
    task_response = get(f"{BACKEND_URL}/task", json=data)
    
    if task_response.status_code == 200:
        task = task_response.json()
        return render_template("info.html", task=task, product_id=product_id)
    return(f"Error {task_response.status_code}")
    
