from flask import Flask
from os import getenv
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = getenv("SECRET_KEY")

app = Flask(__name__)
from . import routes

app.config['SECRET_KEY'] = SECRET_KEY