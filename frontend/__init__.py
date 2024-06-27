from flask import Flask


app = Flask(__name__)
from . import routes

from os import getenv

from dotenv import load_dotenv


load_dotenv()
SECRET_KEY = getenv('SECRET_KEY')

app.config['SECRET_KEY'] = SECRET_KEY