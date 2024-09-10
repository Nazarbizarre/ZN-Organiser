
from .. import app

from flask import Flask, render_template, request, redirect, flash, url_for

from flask_login import current_user, login_required, LoginManager, login_user
from ..forms import RegisterForm, LoginForm
from sqlalchemy import select

from flask_login import login_user
from ..db import Session, User


login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)



@login_manager.user_loader
def load_user(user_id):
    with Session.begin() as session:
        user = session.scalar(select(User).where(User.id == user_id))
        if user:
            user = User(email=user.email)
            return user
    

@app.get('/register')
def register():
    form = RegisterForm()
    return render_template('form_template.html', form=form)


@app.post('/register')
def register_post():
    form = RegisterForm()
    if form.validate_on_submit():
       with Session.begin() as session:
           user = session.scalar(select(User).where(User.email == form.email.data))
           if user:
               flash("User exists!")
               return redirect(url_for('register'))
           pwd = form.password.data
           user = User(
               nickname = form.email.data.split('@')[0],
               email = form.email.data,
               password = pwd,
           )
           session.add(user)
       return redirect(url_for('login'))
    return render_template('form_template.html', form=form)


@app.get('/login')
def login():
    form = LoginForm()
    return render_template('form_template.html', form=form)


@app.post('/login')
def login_post():
    form = LoginForm()
    if form.validate_on_submit():
        with Session.begin() as session:
            user = session.query(User).where(User.nickname == form.nickname.data).first()
            if user:
                if user.password == form.password.data:
                    login_user(user)
                    return redirect(url_for("index"))
                flash("Wrong password")
            else:
                flash("Wrong nickname")
    return render_template('form_template.html', form=form)


@app.post("/users/get_user/<string:email>/<string:password>")
def users_get(email, password):
    with Session.begin() as session:
        user = session.scalar(select(User).where(User.email == email))
        if user and user.password == password:
            return {"context": True}
        else:
            return {"context": False}
        

@app.get("/users/user_email/<string:email>")
def get_by_email(email):
    with Session() as session:
        user = session.query(User).filter(User.email == email).first()
        if user:
            return {"context": True}
        else:
            return {"context": False}
        

@app.post("/users/reminder/<string:email>/<string:time>")
def set_reminder_time(email, time):
    with Session.begin() as session:
        user = session.query(User).filter(User.email == email).first()
        if user:
            user.reminder_time = time
            return {"context": True}
        else:
            return {"context": False}