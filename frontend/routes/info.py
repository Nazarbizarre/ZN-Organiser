

from .. import app, BACKEND_URL

from flask import render_template

from flask_login import login_required

from requests import get, post



@app.get("/task/<int:product_id>")
@login_required
def product(product_id):                    
    tasks_response = get(f"{BACKEND_URL}/get_tasks")
    tasks = tasks_response.json()
    selected_product = None
    
    for task in tasks:
        if task['id'] == product_id:
            selected_product = task
            break

    if selected_product:
        return render_template("info.html", task=selected_product, product_id=product_id)
    else:
        return "Product not found", 404
