

from .. import app, BACKEND_URL

from flask import render_template

from flask_login import login_required

from requests import get, post



@app.get("/task/<int:product_id>")
@login_required
def product(product_id):                    
    tasks_response = get(f"{BACKEND_URL}/task/{product_id}")
    if tasks_response.status_code == 200:
        selected_product = tasks_response.json()
        return render_template("info.html", task=selected_product, product_id=product_id)
    return (f"Error {tasks_response.status_code}")
    
    
