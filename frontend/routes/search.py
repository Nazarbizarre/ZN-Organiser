

from .. import app, BACKEND_URL
from requests import request as request, get
from flask_login import current_user
from flask import render_template, request, redirect, url_for



@app.get('/search')
def search():
    query = request.args.get('query', '')
    if query:
        email = current_user.email
        data = {
            "email": email,
            "completed": False
        }
        tasks = get(f"{BACKEND_URL}/get_tasks", json=data).json()
        filtered = [task for task in tasks if query.lower() in task.get('title').lower()]
        nickname = current_user.email.split("@")[0]
        return render_template("main.html", tasks=filtered, query=query, nickname=nickname)
    else:
        return redirect(url_for("index"))